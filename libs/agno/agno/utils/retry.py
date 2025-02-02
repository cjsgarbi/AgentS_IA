"""Módulo de retry para tentativas de operações com backoff exponencial."""

import time
import random
from functools import wraps
from typing import Any, Callable, TypeVar

T = TypeVar('T')


def retry_with_exponential_backoff(
    max_retries: int = 3,
    initial_wait: float = 1,
    max_wait: float = 60,
    exponential_base: float = 2,
    jitter: bool = True
) -> Callable[[Callable[..., T]], Callable[..., T]]:
    """
    Decorador para retry com backoff exponencial.

    Args:
        max_retries (int): Número máximo de tentativas
        initial_wait (float): Tempo inicial de espera em segundos
        max_wait (float): Tempo máximo de espera em segundos
        exponential_base (float): Base para o cálculo exponencial
        jitter (bool): Se deve adicionar variação aleatória ao tempo de espera

    Returns:
        Callable: Função decorada com retry
    """
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> T:
            wait_time = initial_wait
            last_exception = None

            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    if attempt == max_retries - 1:
                        raise

                    # Calcular próximo tempo de espera
                    wait_time = min(
                        wait_time * exponential_base,
                        max_wait
                    )

                    # Adicionar jitter se necessário
                    if jitter:
                        wait_time *= (0.5 + random.random())

                    time.sleep(wait_time)

            # Não deveria chegar aqui, mas por segurança
            if last_exception:
                raise last_exception
            return None  # type: ignore

        return wrapper
    return decorator
