"""
Logger module for 2GIS MCP Server.
"""

import logging


class LogConfig:
    """Logger configuration class."""

    LOG_FORMAT: str = "%(asctime)s - %(module)s - %(levelname)s - %(message)s"
    DATE_FORMAT: str = "%Y-%m-%d %H:%M:%S"


def setup_logger(
    log_level: int = logging.INFO,
) -> logging.Logger:
    logger = logging.getLogger("")
    logger.setLevel(log_level)

    logger.handlers = []
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter(fmt=LogConfig.LOG_FORMAT, datefmt=LogConfig.DATE_FORMAT))
    logger.handlers = [handler]

    return logger


logger = setup_logger()
