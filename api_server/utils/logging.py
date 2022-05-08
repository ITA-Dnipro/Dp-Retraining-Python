import logging

from common.constants.api import ApiConstants


def setup_logging(name: str, log_level: str = 'DEBUG') -> logging.Logger:
    """Creates Logger objects.
    Args:
        name: of class.
        log_level: string of log level.
    Returns:
    Logger object for specific class.
    """
    logging.basicConfig(format=ApiConstants.LOG_FORMAT.value, level=log_level)
    return logging.getLogger(name)
