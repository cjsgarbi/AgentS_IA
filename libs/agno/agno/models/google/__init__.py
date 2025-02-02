from .gemini import Gemini
from .gemini_openai import GeminiOpenAI
from .gemini_flash import GeminiFlash

__all__ = [
    "Gemini",
    "GeminiOpenAI",
    "GeminiFlash"
]

try:
    from agno.models.google.gemini_openai import GeminiOpenAIChat
except ImportError:

    class GeminiOpenAIChat:  # type: ignore
        def __init__(self, *args, **kwargs):
            raise ImportError(
                "GeminiOpenAI requires the 'openai' library. Please install it via `pip install openai`")
