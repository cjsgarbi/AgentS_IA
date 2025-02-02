"""Módulo para contagem de tokens."""

import tiktoken


def count_tokens(text: str, model: str = "gpt-3.5-turbo") -> int:
    """
    Conta o número de tokens em um texto.

    Args:
        text: Texto para contar tokens
        model: Nome do modelo para usar o encoding apropriado

    Returns:
        Número de tokens no texto
    """
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        encoding = tiktoken.get_encoding("cl100k_base")

    return len(encoding.encode(text))
