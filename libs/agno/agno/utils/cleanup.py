"""Utilitários para limpeza e encerramento gracioso de recursos."""

import atexit
import signal
import sys
from functools import wraps
import logging

# Configurar logging
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)


class GracefulExit:
    """Gerenciador de contexto para encerramento gracioso."""

    def __init__(self):
        self.state = False
        self._original_handlers = {}
        self._registered = False

    def __enter__(self):
        if not self._registered:
            # Registrar handlers
            self._original_handlers[signal.SIGINT] = signal.signal(
                signal.SIGINT, self._handler)
            self._original_handlers[signal.SIGTERM] = signal.signal(
                signal.SIGTERM, self._handler)
            atexit.register(self._cleanup)
            self._registered = True
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._cleanup()
        # Restaurar handlers originais
        for sig, handler in self._original_handlers.items():
            signal.signal(sig, handler)

    def _handler(self, signum, frame):
        """Handler para sinais de interrupção."""
        self.state = True
        # Permitir saída normal
        sys.exit(0)

    def _cleanup(self):
        """Limpar recursos e encerrar graciosamente."""
        try:
            # Limpar buffers
            sys.stdout.flush()
            sys.stderr.flush()

            # Forçar garbage collection
            import gc
            gc.collect()

        except Exception as e:
            logger.error(f"Erro durante limpeza: {e}")
        finally:
            # Suprimir mensagens de erro do gRPC
            logging.getLogger('absl').setLevel(logging.CRITICAL)


def with_graceful_exit(func):
    """Decorator para adicionar encerramento gracioso a funções."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        with GracefulExit():
            return func(*args, **kwargs)
    return wrapper
