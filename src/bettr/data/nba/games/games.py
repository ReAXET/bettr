"""Functions and helpers for retrieving NBA game data for each of the NBA seasons and Teams."""

import logging
import os
from typing import List, Optional, Tuple
from datetime import datetime, timedelta

import pandas as pd
import requests
import numpy as np
from bs4 import BeautifulSoup
from tqdm import tqdm
from pandas import DataFrame

from nba_api.stats.endpoints import TeamGameLogs
from nba_api.stats.static import teams
from nba_api.stats.library.parameters import SeasonAll


from bettr.utilities.paths import DATA_DIR


logger = logging.getLogger(__name__)


def fetch_nba_game_data(start_year=2010, end_year=None, league_id='', team_id='', season_type='Regular Season') -> DataFrame:
    """
    Fetches NBA game data for a range of seasons and compiles it into a DataFrame.

    Parameters:
    start_year (int): The starting year for the data pull. Defaults to 2010.
    end_year (int): The ending year for the data pull. Defaults to the current year.
    league_id (str): The league ID for the data pull. Defaults to NBA.
    team_id (str): The team ID for the data pull. Defaults to all teams.
    season_type (str): The type of season for the data pull. Defaults to 'Regular Season'.

    Returns:
    DataFrame: A pandas DataFrame containing the game data for the specified seasons.
    """

    if end_year is None:
        end_year = datetime.now().year

    # Create a list of all the NBA Seasons needed to be pulled
    seasons_years = list(range(start_year, end_year + 1))
    seasons = [f"{year}-{str(year + 1)[-2:]}" for year in seasons_years]

    # Create an empty dataframe to store all the game data
    games_df = pd.DataFrame()

    # Loop through each season and pull the game data
    for season in seasons:
        logger.info(f"Pulling game data for {season} season")
        games_datapull = TeamGameLogs(
            league_id_nullable=league_id,
            team_id_nullable=team_id,
            season_nullable=season,
            season_type_nullable=season_type,
        )

        games_season = games_datapull.get_data_frames()[0]
        games_df = pd.concat([games_df, games_season], ignore_index=True)

    return games_df


def create_nba_csv_files(start_year=2010, end_year=None, league_id='', team_id='', season_type='Regular Season'):
    """
    Creates CSV files for the NBA game data for a range of seasons.

    Parameters:
    start_year (int): The starting year for the data pull. Defaults to 2010.
    end_year (int): The ending year for the data pull. Defaults to the current year.
    league_id (str): The league ID for the data pull. Defaults to NBA.
    team_id (str): The team ID for the data pull. Defaults to all teams.
    season_type (str): The type of season for the data pull. Defaults to 'Regular Season'.

    Returns:
    None
    """

    # Fetch the game data
    games_df = fetch_nba_game_data(
        start_year=start_year,
        end_year=end_year,
        league_id=league_id,
        team_id=team_id,
        season_type=season_type,
    )

    # Create a list of all the NBA Seasons needed to be pulled
    seasons_years = list(range(start_year + 1))
    seasons = [f"{year}-{str(year + 1)[-2:]}" for year in seasons_years]

    # Create a directory to store the CSV files
    csv_dir = os.path.join(DATA_DIR, 'nba', 'games')
    if csv_dir is not None:
        os.makedirs(csv_dir, exist_ok=True)

    if not os.path.exists(csv_dir):
        os.makedirs(csv_dir)

    # Loop through each season and create a CSV file
    for season in seasons:
        logger.info(f"Creating CSV file for {season} season")
        season_games_df = games_df[games_df['SEASON_ID'] == season]
        season_games_df.to_csv(os.path.join(
            csv_dir, f"{season}.csv"), index=False)


# Create a function to pull the nba data from five thirty eight
def fetch_nba_538_data() -> DataFrame:
    """
    Fetches NBA game data from FiveThirtyEight and compiles it into a DataFrame.

    Parameters:
    None

    Returns:
    DataFrame: A pandas DataFrame containing the game data from FiveThirtyEight.
    """

    # Create a list of all the NBA Seasons needed to be pulled
    seasons_years = list(range(2010, datetime.now().year + 1))
    seasons = [f"{year}-{str(year + 1)[-2:]}" for year in seasons_years]

    # Create an empty dataframe to store all the game data
    games_df = pd.DataFrame()

    # Loop through each season and pull the game data
    for season in seasons:
        logger.info(f"Pulling game data for {season} season")
        url = f"https://projects.fivethirtyeight.com/nba-model/nba_elo.csv"
        df = pd.read_csv(url)
        df['season'] = season
        games_df = pd.concat([games_df, df], ignore_index=True)

    return games_df


# Would be nice to have a function that pulls the data from basketball reference
def fetch_nba_bball_ref_data() -> DataFrame:
    """
    Fetches NBA game data from Basketball Reference and compiles it into a DataFrame.

    Parameters:
    None

    Returns:
    DataFrame: A pandas DataFrame containing the game data from Basketball Reference.
    """

    # Create a list of all the NBA Seasons needed to be pulled
    seasons_years = list(range(2010, datetime.now().year + 1))
    seasons = [f"{year}-{str(year + 1)[-2:]}" for year in seasons_years]

    # Create an empty dataframe to store all the game data
    games_df = pd.DataFrame()

    # Loop through each season and pull the game data
    for season in seasons:
        logger.info(f"Pulling game data for {season} season")
        url = f"https://www.basketball-reference.com/leagues/NBA_{
            season}_games.html"
        df = pd.read_html(url)[0]
        df['season'] = season
        games_df = pd.concat([games_df, df], ignore_index=True)

    return games_df
