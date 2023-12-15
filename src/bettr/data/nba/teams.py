"""Module to retrieve the teams data from the nba_api library. As this is a mostly static dataset, we will only need to
retrieve this data once and store it in our database. We will use the TeamInfoCommon endpoint to retrieve the data."""

from nba_api.stats.endpoints import CommonTeamRoster
import logging
from typing import Any, Dict, List, Optional, Union
from urllib.error import HTTPError
import pandas as pd
from pydantic import BaseModel, Field
from pydantic.types import PositiveInt
from tqdm import tqdm
from bettr.config.settings import Settings

from nba_api.stats.static import teams
from nba_api.stats.endpoints import TeamInfoCommon
from nba_api.stats.library.parameters import SeasonAll

from bettr.utilities import paths

settings = Settings()
nba_teams = teams.get_teams()

# Create a list of team ids
team_ids_dict = {team['full_name']: team['id'] for team in nba_teams}

df = pd.DataFrame()

for team_name, team_id in team_ids_dict.items():
    team_info_common = TeamInfoCommon(team_id=team_id)
    df_team = team_info_common.get_data_frames()[0]
    df_team['TeamName'] = team_name
    df_team['Season'] = SeasonAll.default
    df = pd.concat([df, df_team], ignore_index=True)


# Convert the dataframe to a csv file
df.to_csv(paths.DATA_DIR + "/nba/teams/teams.csv", index=False)


# Create a Roster for each team

# Get the team ids from the teams.csv file
df_teams = pd.read_csv(paths.DATA_DIR + "/nba/teams/teams.csv")

# Create a list of team ids
team_ids = df_teams['TEAM_ID'].tolist()

# List of years to get the roster for
seasons = ['2019-20', '2020-21', '2021-22', '2022-23', '2023-24', '2024-25']

# Create a dataframe to store the roster data
df_roster = pd.DataFrame()

for team_id in tqdm(team_ids):
    for season in seasons:
        common_team_roster = CommonTeamRoster(team_id=team_id, season=season)
        df_roster_team = common_team_roster.get_data_frames()[0]
        df_roster = pd.concat([df_roster, df_roster_team], ignore_index=True)

# Convert the dataframe to a csv file
df_roster.to_csv(paths.DATA_DIR + "/nba/teams/rosters.csv", index=False)
