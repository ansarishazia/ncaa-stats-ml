import pandas as pd
import numpy as np

old_data = pd.read_csv('ncaa_games_07_to_16.csv', parse_dates = ['scheduled_date'])
new_data = pd.read_csv('ncaa_games_13_to_17.csv', parse_dates = ['scheduled_date'])

all_data = pd.concat([
	old_data[['season', 'scheduled_date', 'attendance', 'market', 'name', 'team_id', 'points_game', 'win', 'opp_market', 'opp_name', 'opp_id', 'opp_points_game']],
	new_data[['season', 'scheduled_date', 'attendance', 'market', 'name', 'team_id', 'points_game', 'win', 'opp_market', 'opp_name', 'opp_id', 'opp_points_game']]
])

# There is an overlap between seasons and some games recorded
# This gets rid of the duplicates based on all columns
all_data = all_data.drop_duplicates()

# Write to file
all_data.to_csv('ncaa_consolidated_07_to_17.csv')