"""Implementação do chat para modelos Gemini."""

from typing import List, Iterator, Optional, Dict, Any, Union, AsyncIterator, Callable
import google.generativeai as genai
from os import getenv
import time
from datetime import datetime
import json
import asyncio
from concurrent.futures import ThreadPoolExecutor

from agno.models.base import Message, ModelResponse
from agno.models.gemini.like import GeminiLike
from agno.utils.log import logger
from agno.utils.cache import Cache
from agno.utils.retry import retry_with_exponential_backoff


def simple_token_count(text: str) -> int:
    """Contagem simples de tokens baseada em palavras."""
    return len(text.split())


class GeminiChat(GeminiLike):
    """Implementação do chat para modelos Gemini."""

    # Configurações do modelo
    DEFAULT_CONTEXT_LENGTH = 32768
    MAX_RETRY_ATTEMPTS = 3
    RETRY_INITIAL_WAIT = 1
    RETRY_MAX_WAIT = 60
    AVAILABLE_MODELS = {
        "gemini-pro": "gemini-pro",
        "gemini-pro-vision": "gemini-pro-vision"
    }

    # Configurações de geração padrão
    DEFAULT_GENERATION_CONFIG = {
        "temperature": 0.9,
        "top_p": 1.0,
        "top_k": 1,
        "max_output_tokens": 2048,
    }

    def __init__(self, model_id: str = "gemini-pro"):
        """Inicializa o chat."""
        super().__init__()
        self.id = self.AVAILABLE_MODELS.get(model_id, "gemini-pro")

        # Configurações específicas para o Flash
        if model_id == "gemini-pro-vision":
            self.generation_config = {
                **self.DEFAULT_GENERATION_CONFIG,
                "temperature": 0.7,
                "top_k": 1,
                "candidate_count": 1,
                "stream": True
            }
        else:
            self.generation_config = self.DEFAULT_GENERATION_CONFIG.copy()

        self._validate_and_setup()
        self._setup_cache()
        self._setup_metrics()
        self._history = []
        self._current_message = []

    def _validate_and_setup(self):
        """Valida e configura o ambiente."""
        self.api_key = self.api_key or getenv(
            "GOOGLE_API_KEY") or getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GOOGLE_API_KEY ou GEMINI_API_KEY não definida")

        try:
            genai.configure(api_key=self.api_key)
            self.model = self._create_model()
        except Exception as e:
            logger.error(f"Erro ao configurar Gemini: {str(e)}")
            raise

    def _create_model(self) -> Any:
        """Cria instância do modelo com configurações."""
        return genai.GenerativeModel(
            model_name=self.id,
            generation_config=self.generation_config
        )

    def _setup_cache(self):
        """Configura cache de respostas."""
        self._cache = Cache()
        self._last_request_time = 0
        self._request_count = 0

    def _setup_metrics(self):
        """Configura métricas e telemetria."""
        self._metrics = {
            "total_requests": 0,
            "successful_requests": 0,
            "failed_requests": 0,
            "total_tokens": 0,
            "cache_hits": 0,
            "retry_attempts": 0
        }

    def _validate_messages(self, messages: List[Message]) -> None:
        """Valida lista de mensagens."""
        if not messages:
            raise ValueError("Lista de mensagens vazia")

        total_tokens = sum(simple_token_count(msg.content) for msg in messages)
        if total_tokens > self.context_length:
            raise ValueError(
                f"Total de tokens ({total_tokens}) excede limite ({self.context_length})")

    def _format_error_response(self, error: Exception) -> ModelResponse:
        """Formata resposta de erro."""
        error_msg = f"Erro na resposta: {str(error)}"
        logger.error(error_msg)
        self._metrics["failed_requests"] += 1
        return ModelResponse(content=error_msg)

    @retry_with_exponential_backoff(
        max_retries=MAX_RETRY_ATTEMPTS,
        initial_wait=RETRY_INITIAL_WAIT,
        max_wait=RETRY_MAX_WAIT
    )
    def _send_message(self, chat: Any, message: str, stream: bool = False) -> Any:
        """Envia mensagem com retry logic."""
        try:
            return chat.send_message(message, stream=stream)
        except Exception as e:
            self._metrics["retry_attempts"] += 1
            raise

    def _process_response(self, response: Any) -> Iterator[ModelResponse]:
        """Processa resposta do modelo."""
        if not response:
            raise ValueError("Resposta vazia do modelo")

        if isinstance(response, (list, Iterator)):
            # Streaming response
            for chunk in response:
                if chunk and chunk.text:
                    text = chunk.text.strip()
                    if text:
                        self._metrics["total_tokens"] += simple_token_count(
                            text)
                        yield ModelResponse(content=text)
        else:
            # Non-streaming response
            if not response.text:
                raise ValueError("Texto da resposta vazio")

            text = response.text.strip()
            if text:
                self._metrics["total_tokens"] += simple_token_count(text)
                yield ModelResponse(content=text)

        self._metrics["successful_requests"] += 1

    def invoke(self, messages: List[Message]) -> ModelResponse:
        """Invoca o modelo de forma síncrona."""
        response = None
        for chunk in self.invoke_stream(messages):
            if response is None:
                response = chunk
            else:
                response.content += chunk.content
        return response or ModelResponse(content="")

    def invoke_stream(self, messages: List[Message]) -> Iterator[ModelResponse]:
        """Invoca o modelo em modo streaming."""
        return self.response_stream(messages)

    async def ainvoke(self, messages: List[Message]) -> ModelResponse:
        """Invoca o modelo de forma assíncrona."""
        response = None
        async for chunk in self.ainvoke_stream(messages):
            if response is None:
                response = chunk
            else:
                response.content += chunk.content
        return response or ModelResponse(content="")

    async def ainvoke_stream(self, messages: List[Message]) -> AsyncIterator[ModelResponse]:
        """Invoca o modelo em modo streaming assíncrono."""
        async for chunk in self.aresponse_stream(messages):
            yield chunk

    def response(self, messages: List[Message]) -> ModelResponse:
        """Gera resposta de forma síncrona."""
        return self.invoke(messages)

    async def aresponse(self, messages: List[Message]) -> ModelResponse:
        """Gera resposta de forma assíncrona."""
        return await self.ainvoke(messages)

    def _handle_rate_limiting(self):
        """Gerencia rate limiting."""
        current_time = time.time()
        if current_time - self._last_request_time < 1:
            time.sleep(1 - (current_time - self._last_request_time))
        self._last_request_time = time.time()

    def prepare_messages(self, messages: List[Dict[str, str]]) -> List[Dict[str, Any]]:
        """Prepara mensagens para o formato do Gemini."""
        formatted = []
        for msg in messages:
            formatted.append({
                "parts": [{
                    "text": msg["content"]
                }],
                "role": "user" if msg["role"] == "user" else "model"
            })
        return formatted

    def _prepare_chat_messages(self, messages: List[Message]) -> List[Any]:
        """Prepara mensagens para o chat."""
        formatted_messages = []
        for msg in messages[:-1]:
            formatted = self.prepare_messages([{
                "role": msg.role,
                "content": msg.content
            }])
            formatted_messages.extend(formatted)
        return formatted_messages

    def _check_cache(self, cache_key: str) -> Optional[ModelResponse]:
        """Verifica e retorna resposta do cache se existir."""
        if cached := self._cache.get(cache_key):
            self._metrics["cache_hits"] += 1
            return ModelResponse(content=cached)
        return None

    def _process_chat_response(self, response: Any, cache_key: str) -> Iterator[ModelResponse]:
        """Processa a resposta do chat e gerencia cache."""
        response_text = ""
        for chunk in self._process_response(response):
            response_text += chunk.content
            yield chunk
        if response_text:
            self._cache.set(cache_key, response_text)

    def response_stream(self, messages: List[Message]) -> Iterator[ModelResponse]:
        """Gera resposta em streaming."""
        try:
            self._metrics["total_requests"] += 1
            self._validate_messages(messages)
            cache_key = json.dumps([msg.content for msg in messages])

            if cached_response := self._check_cache(cache_key):
                yield cached_response
                return

            self._handle_rate_limiting()
            formatted_messages = self._prepare_chat_messages(messages)
            chat = self.model.start_chat(history=formatted_messages)
            current_message = messages[-1].content

            response = self._send_message(
                chat, current_message,
                stream=(self.id == "gemini-pro-vision")
            )

            self._history = formatted_messages
            self._current_message = [current_message]
            yield from self._process_chat_response(response, cache_key)

        except Exception as e:
            yield self._format_error_response(e)

    async def aresponse_stream(self, messages: List[Message]) -> AsyncIterator[ModelResponse]:
        """Versão assíncrona do response_stream."""
        with ThreadPoolExecutor() as executor:
            async for chunk in self._async_iterator(
                executor, self.response_stream, messages
            ):
                yield chunk

    async def _async_iterator(
        self, executor: ThreadPoolExecutor, func: Callable, *args: Any, **kwargs: Any
    ) -> AsyncIterator[Any]:
        """Helper para converter um iterator síncrono em assíncrono."""
        loop = asyncio.get_event_loop()
        for item in await loop.run_in_executor(executor, func, *args, **kwargs):
            yield item

    def get_history(self) -> List[Dict[str, Any]]:
        """Retorna histórico do chat."""
        return self._history

    def clear_history(self) -> None:
        """Limpa histórico do chat."""
        self._history.clear()
        self._current_message.clear()

    def get_metrics(self) -> Dict[str, Union[int, float]]:
        """Retorna métricas do chat."""
        return self._metrics

    def reset_metrics(self) -> None:
        """Reseta métricas do chat."""
        self._setup_metrics()

    @property
    def context_length(self) -> int:
        """Retorna o tamanho do contexto do modelo."""
        return self.DEFAULT_CONTEXT_LENGTH

    @property
    def is_chat(self) -> bool:
        """Indica se é um modelo de chat."""
        return True
