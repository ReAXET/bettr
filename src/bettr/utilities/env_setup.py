"""Enum Class for production, development and testing environments."""
import os
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Literal, Optional, Tuple, Union


class Env(Enum):
    """Enum Class for production, development and testing environments."""

    PRODUCTION = 'production'
    DEVELOPMENT = 'development'
    TESTING = 'testing'
    LOCAL = 'local'
    STAGING = 'staging'

    def __str__(self) -> Literal['production', 'development', 'testing', 'local', 'staging']:
        return self.value


def get_env() -> Env:
    """Get the current environment."""
    return Env(os.getenv('ENV', 'local'))


if get_env():
    from dotenv import load_dotenv
    load_dotenv()
