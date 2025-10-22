"""
Configuración del sistema de logging.
"""

import logging
import sys
from pathlib import Path


def setup_logger(name: str = __name__, level: int = logging.INFO) -> logging.Logger:
    """
    Configura y retorna un logger.

    Args:
        name (str): Nombre del logger.
        level (int): Nivel de logging.

    Returns:
        logging.Logger: Logger configurado.
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Evitar duplicar handlers
    if logger.handlers:
        return logger

    # Handler para consola
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)

    # Formato
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    console_handler.setFormatter(formatter)

    logger.addHandler(console_handler)

    return logger
