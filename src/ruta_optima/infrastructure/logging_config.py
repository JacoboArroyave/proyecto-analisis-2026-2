"""Configuracion centralizada del logging de la aplicacion."""

import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path


APPLICATION_LOGGER = "ruta_optima"
LOG_FORMAT = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def configure_logging(log_directory: Path, level: int = logging.DEBUG) -> Path:
    """Configura consola y archivo rotativo; devuelve la ruta del archivo activo."""
    log_directory.mkdir(parents=True, exist_ok=True)
    log_file = log_directory / "ruta_optima.log"
    logger = logging.getLogger(APPLICATION_LOGGER)

    for handler in logger.handlers[:]:
        handler.close()
        logger.removeHandler(handler)

    logger.setLevel(level)
    logger.propagate = False

    formatter = logging.Formatter(LOG_FORMAT, datefmt=DATE_FORMAT)
    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=1_000_000,
        backupCount=3,
        encoding="utf-8",
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    logger.info("Logging configurado; archivo activo: %s", log_file)
    return log_file