"""Logger de aplicacion con archivos historicos, ultimo log y consola colorida."""

import copy
import logging
import sys
from datetime import datetime
from functools import wraps
from pathlib import Path
from typing import Any, Callable, ParamSpec, TypeVar

try:
    from colorama import Fore, Style, init
except ImportError:  # pragma: no cover - solo aplica sin dependencias instaladas
    class _NoColor:
        LIGHTBLACK_EX = "\033[90m"
        BLUE = "\033[34m"
        YELLOW = "\033[33m"
        RED = "\033[31m"
        MAGENTA = "\033[35m"
        BRIGHT = "\033[1m"
        RESET_ALL = "\033[0m"

    Fore = Style = _NoColor()

    def init(*args: Any, **kwargs: Any) -> None:
        """Fallback para ejecutar sin colorama instalada."""

from ruta_optima.constants.base import APPLICATION_LOGGER_NAME, DATE_FORMAT, LOGS_PATH

P = ParamSpec("P")
R = TypeVar("R")


class ColorFormatter(logging.Formatter):
    """Formatter de consola que colorea solo el nombre del nivel."""

    COLORS = {
        logging.DEBUG: Fore.LIGHTBLACK_EX,
        logging.INFO: Fore.BLUE,
        logging.WARNING: Fore.YELLOW,
        logging.ERROR: Fore.RED,
        logging.CRITICAL: Fore.MAGENTA + Style.BRIGHT,
    }

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        init(autoreset=True)

    def format(self, record: logging.LogRecord) -> str:
        colored_record = copy.copy(record)
        color = self.COLORS.get(record.levelno, "")
        colored_record.levelname = f"{color}{record.levelname}{Style.RESET_ALL}"
        return super().format(colored_record)


class SafeLogger:
    """Logger con archivo historico, ultimo log y salida de consola."""

    def __init__(
        self,
        name: str,
        logs_path: Path = LOGS_PATH,
        level: int = logging.DEBUG,
    ) -> None:
        self._logger = self._setup_logger(name, logs_path, level)

    def _setup_logger(self, name: str, logs_path: Path, level: int) -> logging.Logger:
        current_time = datetime.now()
        hour_dir = (
            Path(logs_path)
            / current_time.strftime("%d_%m_%Y")
            / f"{current_time.strftime('%H')}hrs"
        )
        hour_dir.mkdir(parents=True, exist_ok=True)

        detailed_log_file = hour_dir / f"{name}.log"
        last_log_file = Path(logs_path) / f"last_{name}.log"
        last_log_file.parent.mkdir(parents=True, exist_ok=True)

        logger = logging.getLogger(name)
        logger.setLevel(level)
        logger.propagate = False
        for handler in logger.handlers[:]:
            handler.close()
            logger.removeHandler(handler)

        plain_formatter = logging.Formatter(
            "%(asctime)s [%(name)s] %(levelname)s %(processName)s: %(message)s",
            datefmt=DATE_FORMAT,
        )
        colored_formatter = ColorFormatter(
            "%(levelname)s (%(asctime)s): %(message)s",
            datefmt="%H:%M:%S",
        )

        detailed_handler = logging.FileHandler(
            detailed_log_file,
            mode="w",
            encoding="utf-8",
        )
        detailed_handler.setLevel(logging.DEBUG)
        detailed_handler.setFormatter(plain_formatter)

        last_handler = logging.FileHandler(
            last_log_file,
            mode="w",
            encoding="utf-8",
        )
        last_handler.setLevel(logging.DEBUG)
        last_handler.setFormatter(plain_formatter)

        # stderr mantiene stdout limpio para que la CLI pueda emitir JSON valido.
        console_handler = logging.StreamHandler(sys.stderr)
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(colored_formatter)

        logger.addHandler(detailed_handler)
        logger.addHandler(last_handler)
        logger.addHandler(console_handler)
        return logger

    def debug(self, message: object, *args: object) -> None:
        self._logger.debug(self._safe_message(message), *args)

    def info(self, message: object, *args: object) -> None:
        self._logger.info(self._safe_message(message), *args)

    def warning(self, message: object, *args: object) -> None:
        self._logger.warning(self._safe_message(message), *args)

    def error(self, message: object, *args: object) -> None:
        self._logger.error(self._safe_message(message), *args)

    def critical(self, message: object, *args: object) -> None:
        self._logger.critical(self._safe_message(message), *args)

    def _safe_message(self, message: object) -> str:
        try:
            return str(message).encode("utf-8", errors="replace").decode("utf-8")
        except Exception:
            return "[Objeto no representable]"


def get_logger(
    name: str = APPLICATION_LOGGER_NAME,
    logs_path: Path = LOGS_PATH,
    level: int = logging.DEBUG,
) -> SafeLogger:
    """Crea un logger con la estructura de archivos del proyecto."""
    return SafeLogger(name, logs_path, level)


def configure_logging(
    log_directory: Path = LOGS_PATH,
    level: int = logging.DEBUG,
) -> SafeLogger:
    """Configura y devuelve el logger principal para inyeccion de dependencias."""
    logger = get_logger(APPLICATION_LOGGER_NAME, log_directory, level)
    logger.info("Logging configurado; directorio activo: %s", log_directory)
    return logger


def log_execution(logger: SafeLogger) -> Callable[[Callable[P, R]], Callable[P, R]]:
    """Decorador opcional para registrar inicio, fin y errores de una funcion."""

    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        @wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            logger.debug("Iniciando %s", func.__name__)
            try:
                result = func(*args, **kwargs)
            except Exception as error:
                logger.error("Error en %s: %s", func.__name__, error)
                raise
            logger.debug("Completado %s", func.__name__)
            return result

        return wrapper

    return decorator
