from getpass import getuser
import os
from pathlib import Path
from typing import List, Optional

from dotenv import load_dotenv
from pydantic import BaseSettings, Field

from bettr.config.settings import Settings
from bettr.utilities.paths import DATA_DIR

load_dotenv()


# def a postgres url function
def sync_postgres_url(
    user: str = getuser(),
    fallback_hosts: Optional[List[str]] | None = None,
    driver: str = 'psycopg2',
    password: str = os.getenv.get('POSTGRES_PASSWORD'),
    host: str = os.getenv.get('POSTGRES_HOST'),
    port: str = os.getenv.get('POSTGRES_PORT'),
    database: str = os.getenv.get('POSTGRES_DB'),
    **kwargs,
) -> str:
    """Returns a postgres url."""
    url = f"postgresql+{driver}://{user}:{password}@{host}:{port}/{database}"

    if password is not None:
        url += f":{password}"

    url += f"@{host}"

    if port is not None:
        url += f":{port}"

    url += f"/{database}"
    options = [f'host={host}' for host in fallback_hosts or []]
    options.extend(f'{key}={value}' for key, value in kwargs.items())

    if len(options) > 0:
        url += f"?{'&'.join(options)}"
    return url


# Define a sqlite url function
def sqlite_url(dbfile: str = 'bettr.db') -> Optional[str]:
    """Returns a sqlite url."""
    url = f"sqlite:///{DATA_DIR}/{dbfile}"
    if os.path.exists(url):
        return url
    return None


# Define an async postgres url function
def async_postgres_url(
    user: str = getuser(),
    fallback_hosts: Optional[List[str]] | None = None,
    driver: str = 'asyncpg',
    password: str = os.getenv.get('POSTGRES_PASSWORD'),
    host: str = os.getenv.get('POSTGRES_HOST'),
    port: str = os.getenv.get('POSTGRES_PORT'),
    database: str = os.getenv.get('POSTGRES_DB'),
    **kwargs,
) -> str:
    """Returns an async postgres url."""
    url = f"postgresql+{driver}://{user}:{password}@{host}:{port}/{database}"

    if password is not None:
        url += f":{password}"

    url += f"@{host}"

    if port is not None:
        url += f":{port}"

    url += f"/{database}"
    options = [f'host={host}' for host in fallback_hosts or []]
    options.extend(f'{key}={value}' for key, value in kwargs.items())

    if len(options) > 0:
        url += f"?{'&'.join(options)}"
    return url
