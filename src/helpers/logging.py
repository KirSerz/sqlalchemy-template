import logging
import sys

from core.env import LOG_LEVEL, LOG_FORMAT


_log_format = LOG_FORMAT


def get_stream_handler(stream=sys.stderr) -> logging.StreamHandler:
    stream_handler = logging.StreamHandler(stream)
    return stream_handler


def get_logger(
    name: str = "",
    level: str = "INFO",
    business_handler: bool = False,
    log_format: str = _log_format,
) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(level)
    handler = (
        get_stream_handler()
        if business_handler is False
        else get_stream_handler(sys.stdout)
    )
    handler.setLevel(level)
    handler.setFormatter(logging.Formatter(log_format))
    logger.addHandler(handler)
    return logger


logger = get_logger(level=LOG_LEVEL)
