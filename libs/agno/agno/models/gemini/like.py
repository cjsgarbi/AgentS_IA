"""Interface base para modelos compatíveis com Gemini."""

from dataclasses import dataclass, field
from typing import Optional, List, Iterator, Dict, Any
from agno.models.base import Message, ModelResponse, Model


@dataclass
class GeminiLike(Model):
    """Base class for Gemini models."""

    # Model configuration
    DEFAULT_CONTEXT_LENGTH: int = 32768
    MAX_RETRY_ATTEMPTS: int = 3
    RETRY_INITIAL_WAIT: int = 1
    RETRY_MAX_WAIT: int = 60

    AVAILABLE_MODELS: Dict[str, str] = field(default_factory=lambda: {
        "gemini-pro": "gemini-pro",
        "gemini-2.0.0-flash": "gemini-flash"
    })

    # Default generation config
    DEFAULT_GENERATION_CONFIG: Dict[str, Any] = field(default_factory=lambda: {
        "temperature": 1.0,
        "top_p": 0.95,
        "top_k": 64,
        "max_output_tokens": 8192,
        "response_mime_type": "text/plain",
    })

    id: str = "gemini-pro"
    name: str = "Gemini"
    provider: str = "Google"

    api_key: Optional[str] = None
    temperature: float = 0.7
    max_tokens: Optional[int] = None
    top_p: float = 1.0
    top_k: int = 1

    _history: List[Dict[str, Any]] = field(default_factory=list)
    _current_message: List[str] = field(default_factory=list)

    def __post_init__(self):
        """Validação após inicialização."""
        if self.id not in self.AVAILABLE_MODELS:
            raise ValueError(
                f"Modelo {self.id} não disponível. Opções: {list(self.AVAILABLE_MODELS.keys())}")

        self.name = self.AVAILABLE_MODELS[self.id]
        self._context_length = self.DEFAULT_CONTEXT_LENGTH

    @property
    def context_length(self) -> int:
        """Retorna o tamanho do contexto do modelo."""
        return self._context_length

    def prepare_messages(self, messages: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Prepare messages for the model.

        Args:
            messages (List[Dict[str, Any]]): Messages to prepare.

        Returns:
            List[Dict[str, Any]]: Prepared messages.
        """
        prepared_messages = []
        for message in messages:
            if message.get("role") == "system":
                # Convert system messages to user messages for Gemini
                prepared_messages.append({
                    "role": "user",
                    "content": message["content"]
                })
            else:
                prepared_messages.append(message)
        return prepared_messages

    def get_model_config(self) -> Dict[str, Any]:
        """Retorna configuração do modelo."""
        return {
            "temperature": self.temperature,
            "top_p": self.top_p,
            "top_k": self.top_k,
            "max_output_tokens": self.max_tokens
        }

    def get_api_key(self) -> str:
        """Retorna a chave API."""
        if not self.api_key:
            raise ValueError("API key não configurada")
        return self.api_key

    def response_stream(self, messages: List[Message]) -> Iterator[ModelResponse]:
        """Método base para streaming de respostas."""
        raise NotImplementedError

    def add_images_to_message(self, message: Any, images: List[str]) -> Any:
        """
        Add images to a message.

        Args:
            message (Any): The message to add images to.
            images (List[str]): List of image paths or URLs.

        Returns:
            Any: The message with added images.
        """
        # TODO: Implement image handling
        return message

    def add_audio_to_message(self, message: Any, audio: str) -> Any:
        """
        Add audio to a message.

        Args:
            message (Any): The message to add audio to.
            audio (str): Audio path or URL.

        Returns:
            Any: The message with added audio.
        """
        # TODO: Implement audio handling
        return message
