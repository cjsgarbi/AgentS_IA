from dataclasses import dataclass
from os import getenv
from typing import Optional, List, Dict, Any, Iterator
import google.generativeai as genai
from agno.models.openai.like import OpenAILike
from agno.models.base import Message, ModelResponse
from agno.utils.log import logger


@dataclass
class GeminiFlash(OpenAILike):
    """
    Classe para interagir com os modelos Gemini Flash do Google.

    Atributos:
        id (str): O ID do modelo Gemini a ser usado. Padrão é "gemini-1.5-flash".
        name (str): O nome deste modelo de chat. Padrão é "Gemini Flash".
        provider (str): O provedor do modelo. Padrão é "Google".
        api_key (str): A chave API para autorizar requisições ao Gemini.
        temperature (float): Temperatura para geração de texto. Padrão é 0.7.
        max_tokens (Optional[int]): Número máximo de tokens. Padrão é None.
        top_p (float): Valor de top_p para amostragem. Padrão é 1.0.
        top_k (int): Valor de top_k para amostragem. Padrão é 1.
    """

    id: str = "gemini-1.5-flash"
    name: str = "Gemini Flash"
    provider: str = "Google"

    api_key: Optional[str] = getenv("GOOGLE_API_KEY")
    temperature: float = 0.7
    max_tokens: Optional[int] = None
    top_p: float = 1.0
    top_k: int = 1

    def __post_init__(self):
        super().__post_init__()
        if not self.api_key:
            logger.error(
                "GOOGLE_API_KEY não definida. Por favor, defina a variável de ambiente GOOGLE_API_KEY.")
            raise ValueError("GOOGLE_API_KEY não definida")
        try:
            genai.configure(api_key=self.api_key)
        except Exception as e:
            logger.error(f"Erro ao configurar cliente Gemini: {str(e)}")
            raise

    def _create_chat(self, messages: List[Message]) -> Any:
        """Cria uma sessão de chat com o Gemini"""
        try:
            model = genai.GenerativeModel(
                model_name=self.id,
                generation_config={
                    "temperature": self.temperature,
                    "top_p": self.top_p,
                    "top_k": self.top_k,
                    "max_output_tokens": self.max_tokens
                }
            )

            # Converter mensagens para o formato do Gemini
            gemini_messages = []
            for msg in messages:
                role = msg["role"]
                content = msg["content"]

                if role == "system":
                    gemini_messages.append(
                        {"role": "user", "content": content})
                else:
                    gemini_messages.append({"role": role, "content": content})

            return model.start_chat(history=gemini_messages)
        except Exception as e:
            logger.error(f"Erro ao criar chat Gemini: {str(e)}")
            raise

    def response_stream(self, messages: List[Message]) -> Iterator[ModelResponse]:
        """
        Gera uma resposta em streaming usando o modelo Gemini.

        Args:
            messages: Lista de mensagens no formato do Agno

        Yields:
            ModelResponse: Chunks da resposta do modelo
        """
        logger.debug(
            f"---------- {self.get_provider()} Response Start ----------")

        try:
            chat = self._create_chat(messages)
            response = chat.send_message(
                messages[-1]["content"],
                stream=True
            )

            for chunk in response:
                if chunk.text:
                    yield ModelResponse(
                        content=chunk.text,
                        role="assistant",
                        metadata={}
                    )

        except Exception as e:
            logger.error(f"Erro ao gerar resposta do Gemini: {str(e)}")
            yield ModelResponse(
                content=f"Erro ao gerar resposta: {str(e)}",
                role="assistant",
                metadata={"error": str(e)}
            )

        logger.debug(
            f"---------- {self.get_provider()} Response End ----------")

    async def aresponse_stream(self, messages: List[Message]) -> Iterator[ModelResponse]:
        """
        Versão assíncrona do response_stream.
        Por enquanto, usa a versão síncrona pois o Gemini ainda não tem suporte assíncrono oficial.
        """
        return self.response_stream(messages)

    @property
    def context_length(self) -> int:
        """Retorna o tamanho máximo do contexto para o modelo Gemini Pro"""
        return 32768  # Aproximadamente 32k tokens

    @property
    def is_chat(self) -> bool:
        return True
