"""Constantes globales centralizadas de la aplicacion."""

import logging
from pathlib import Path


DEFAULT_SCENARIO_PATH = Path("data/entrada_G3_mochila_20_nodos.json")
LOGS_PATH = Path("logs")
DEFAULT_LOG_DIRECTORY = Path("logs")
DEFAULT_LOG_LEVEL = logging.DEBUG
APPLICATION_LOGGER_NAME = "ruta_optima"
LOG_FORMAT = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
LOG_MAX_BYTES = 1_000_000
LOG_BACKUP_COUNT = 3