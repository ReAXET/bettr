"""Custom Logging Module for Bettr"""

import logging
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional, Any, Dict
import json
import re
import uuid
from platform import platform, python_version


from rich.logging import RichHandler
from rich.traceback import install as rich_traceback_install
from rich.console import Console


from bettr.config.settings import Settings



LOG_DIR = Path(__file__).parent.parent.parent / "logs"
LOG_DIR.mkdir(exist_ok=True)

LOG_FILE = LOG_DIR / f"{datetime.now().strftime('%Y-%m-%d')}.log"


LOGGING_FORMAT = (
    "%(asctime)s | %(levelname)s | %(name)s:%(funcName)s:%(lineno)d - %(message)s"
)

LOGGING_LEVEL = logging.DEBUG if Settings.DEBUG else logging.INFO

log_traces = rich_traceback_install(show_locals=True, width=120, word_wrap=True)

console = Console()


class BettrLogger:
    """Custom logging class for Bettr utilizing the Rich library for both console and file logging."""

    def __init__(
        self,
        name: str,
        level: int = LOGGING_LEVEL,
        format: str = LOGGING_FORMAT,
        log_file: Optional[str] = Settings.LOG_FILE,
        log_traces: bool = Settings.LOG_TRACES,
        log_dir: str = Settings.LOG_FILE,
        **kwargs,
    ) -> None:
        """Initializes the BettrLogger class.

        Parameters:
        name (str): The name of the logger.
        level (int): The logging level for the logger.
        format (str): The logging format for the logger.
        log_file (str): The path to the log file.
        log_traces (bool): Whether to log traces or not.
        log_dir (str): The path to the log directory.
        """
        self.name = name
        self.level = level
        self.format = format
        self.log_file = log_file
        self.log_traces = log_traces
        self.log_dir = log_dir
        self.kwargs = kwargs

        self.logger = logging.getLogger(self.name)
        self.logger.setLevel(self.level)

        self.formatter = logging.Formatter(self.format)

        self.file_handler = logging.FileHandler(self.log_file) # type: ignore
        self.file_handler.setLevel(self.level)
        self.file_handler.setFormatter(self.formatter)

        self.stream_handler = RichHandler(
            console=console,
            show_time=False,
            show_path=False,
            markup=True,
            rich_tracebacks=self.log_traces,
        )
        self.stream_handler.setLevel(self.level)
        self.stream_handler.setFormatter(self.formatter)

        self.logger.addHandler(self.file_handler)
        self.logger.addHandler(self.stream_handler)

    def log(self, level: int, message: str, *args, **kwargs) -> None:
        """Logs a message to the logger.

        Parameters:
        level (int): The logging level for the message.
        message (str): The message to log.
        """
        self.logger.log(level, message, *args, **kwargs)

    def debug(self, message: str, *args, **kwargs) -> None:
        """Logs a debug message to the logger.

        Parameters:
        message (str): The message to log.
        """
        self.logger.debug(message, *args, **kwargs)

    def info(self, message: str, *args, **kwargs) -> None:
        """Logs an info message to the logger.

        Parameters:
        message (str): The message to log.
        """

        self.logger.info(message: str, *args, **kwargs)

    def warning(self, message: str, *args, **kwargs) -> None:
        """Logs a warning message to the logger.

        Parameters:
        message (str): The message to log.
        """
        self.logger.warning(message, *args, **kwargs)


    def error(self, message: str, *args, **kwargs) -> None:
        """Logs an error message to the logger.

        Parameters:
        message (str): The message to log.
        """
        self.logger.error(message, *args, **kwargs)

    def critical(self, message: str, *args, **kwargs) -> None:
        """Logs a critical message to the logger.

        Parameters:
        message (str): The message to log.
        """
        self.logger.critical(message, *args, **kwargs)

    def exception(self, message: str, *args, **kwargs) -> None:
        """Logs an exception message to the logger.

        Parameters:
        message (str): The message to log.
        """
        self.logger.exception(message, *args, **kwargs)


def get_logger(name: str, **kwargs) -> BettrLogger:
    """Returns a logger.

    Parameters:
    name (str): The name of the logger.

    Returns:
    BettrLogger: The logger class.
    """
    return BettrLogger(name, **kwargs)


logger = get_logger(__name__)



