import pandas as pd
import numpy as np

from google.cloud import bigquery as bq

client = bq.Client()
dataset_reference = client.dataset('ncaa_basketball', project = 'bigquery-public-data')
ncaa_data = client.get_dataset(dataset_reference)

tables = client.list_tables(ncaa_data)

query = 'select season, scheduled_date, attendance, market, name, team_id, points_game, win, opp_market, opp_name, opp_id, opp_points_game from `bigquery-public-data.ncaa_basketball.mbb_historical_teams_games` where season > 2006'
job = client.query(query)
games_since_2006 = job.to_dataframe()

# This data set contains game stats from 2007 - 2016ish
# Each game in entered twice for each team
# Does not contain stats like FG, 3PT, rebounds, fouls etc. as they are not recorded
games_since_2006.to_csv('ncaa_games_07_to_16.csv')

query = 'select game_id, season, scheduled_date, attendance, home_team, name, market, team_id, opp_name, opp_market, opp_id, win, points_game, minutes, opp_points_game, opp_minutes from `bigquery-public-data.ncaa_basketball.mbb_teams_games_sr`'
job = client.query(query)
games_2013_2018 = job.to_dataframe()

# This data set contains game stats from 2013-2017
# Each game is entered twice for each team
# Does not contain stats like FG, 3PT, rebounds, fouls etc. but can be added to the query
games_2013_2018.to_csv('ncaa_games_13_to_17.csv')