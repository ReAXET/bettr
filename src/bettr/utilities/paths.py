"""Module to set the proper paths, including ROOT_DIR, DATA_DIR, and LOG_DIR."""
import os
from pathlib import Path

from dotenv import load_dotenv
from bettr.config.settings import Settings

settings = Settings()

print(Settings().ROOT_DIR)

load_dotenv()

# Root directory
ROOT_DIR: Path = Path(__file__).parents[3]

# Data directory
DATA_DIR: str = os.path.join(ROOT_DIR, "src/bettr/data")

# Config directory
CONFIG_DIR: str = os.path.join(ROOT_DIR, "src/bettr/config")

# DB directory
DB_DIR: str = os.path.join(ROOT_DIR, "src/bettr/database")

# Logs directory
LOGS_DIR: str = os.path.join(ROOT_DIR, "src/bettr/logs")

# Models directory
MODELS_DIR: str = os.path.join(ROOT_DIR, "src/bettr/models")

# Tests directory
TESTS_DIR: str = os.path.join(ROOT_DIR, "src/bettr/tests")

# Utilities directory
UTILITIES_DIR: str = os.path.join(ROOT_DIR, "src/bettr/utilities")

# API directory
API_DIR: str = os.path.join(ROOT_DIR, "src/bettr/api")

# Static directory
STATIC_DIR: str = os.path.join(ROOT_DIR, "src/bettr/static")

# Templates directory
TEMPLATES_DIR: str = os.path.join(ROOT_DIR, "src/bettr/templates")

# Schema directory
SCHEMA_DIR: str = os.path.join(ROOT_DIR, "src/bettr/schema")

# Core directory
CORE_DIR: str = os.path.join(ROOT_DIR, "src/bettr/core")


# Create a send_df_to_csv function
def send_df_to_csv(df, data_dir, filename):
    """Create a send_df_to_csv function

    Args:
        df (pl.DataFrame): Polars dataframe to send to csv.
        data_dir (str): Directory to send the csv file to.
        filename (str): Name of the csv file to be created.
    """
    df.to_csv(os.path.join(data_dir, filename))
