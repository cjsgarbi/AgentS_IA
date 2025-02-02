"""Módulo de cache para armazenamento temporário de respostas."""

from typing import Any, Optional
from datetime import datetime, timedelta


class Cache:
    """Implementação simples de cache em memória com expiração."""

    def __init__(self, ttl_seconds: int = 3600):
        """
        Inicializa o cache.

        Args:
            ttl_seconds (int): Tempo de vida dos itens em segundos. Padrão: 1 hora
        """
        self._cache = {}
        self._ttl = ttl_seconds

    def get(self, key: str) -> Optional[Any]:
        """
        Recupera um item do cache.

        Args:
            key (str): Chave do item

        Returns:
            Optional[Any]: Valor armazenado ou None se não encontrado/expirado
        """
        if key not in self._cache:
            return None

        item = self._cache[key]
        if datetime.now() > item["expires"]:
            del self._cache[key]
            return None

        return item["value"]

    def set(self, key: str, value: Any) -> None:
        """
        Armazena um item no cache.

        Args:
            key (str): Chave do item
            value (Any): Valor a ser armazenado
        """
        self._cache[key] = {
            "value": value,
            "expires": datetime.now() + timedelta(seconds=self._ttl)
        }

    def clear(self) -> None:
        """Limpa todo o cache."""
        self._cache.clear()

    def remove(self, key: str) -> None:
        """
        Remove um item específico do cache.

        Args:
            key (str): Chave do item a ser removido
        """
        if key in self._cache:
            del self._cache[key]
