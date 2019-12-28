import pandas as pd
import numpy as np

from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline

pd.set_option('display.expand_frame_repr', False)

def get_attendance_diff(diff):
	return 'UP' if (diff > 0) else 'DOWN'

def transform_bool_to_binary(win):
	return 1 if win else 0

data = pd.read_csv('ncaa_consolidated_07_to_17.csv', usecols = ['scheduled_date', 'team_id', 'points_game', 'opp_points_game', 'win', 'attendance'], parse_dates = ['scheduled_date'])
data = data.dropna()

# Add margin game was won/lost by
data['margin'] = data['points_game'] - data['opp_points_game']

# Transform win boolean to 1,0
data['win_binary'] = data['win'].apply(transform_bool_to_binary)

data = data.sort_values(by = ['team_id', 'scheduled_date'])

# Get next game attendance
attendance = data[['team_id', 'attendance']].shift(-1)
attendance.columns = ['team_id_next', 'attendance_next']

# Join
data = pd.concat([data, attendance], axis=1).dropna()

# Remove matching between two different teams
data = data[data['team_id'] == data['team_id_next']]
data['attendance_diff'] = data['attendance_next'] - data['attendance']

# Classify increase or decrease in attendance
data['attendance_diff'] = data['attendance_diff'].apply(get_attendance_diff)

# Prepare ML data
X = data[['attendance', 'points_game', 'win_binary', 'margin']]
y = data['attendance_diff']
X_train, X_test, y_train, y_test = train_test_split(X, y)

# GaussianNB
gaussian_model = make_pipeline(StandardScaler(), GaussianNB(priors=None))
gaussian_model.fit(X_train, y_train)

print('GaussianNB training score: {}'.format(gaussian_model.score(X_train, y_train)))
print('GaussianNB validation score: {}'.format(gaussian_model.score(X_test, y_test)))

# Decision Tree
tree_model = make_pipeline(StandardScaler(), DecisionTreeClassifier(max_depth = 17))
tree_model.fit(X_train, y_train)

print('Decision Tree training score: {}'.format(tree_model.score(X_train, y_train)))
print('Decision Tree validation score: {}'.format(tree_model.score(X_test, y_test)))