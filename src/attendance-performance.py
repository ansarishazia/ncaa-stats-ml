import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats

pd.set_option('display.expand_frame_repr', False)

data = pd.read_csv('ncaa_consolidated_07_to_17.csv', usecols = ['team_id', 'points_game', 'opp_points_game', 'win', 'attendance'])
data = data.dropna()

avg_attendance = data.groupby('team_id').mean()['attendance']
avg_points_game = data.groupby('team_id').mean()['points_game']

plt.xlabel('Average attendance per game')
plt.ylabel('Avergae points per game')
plt.plot(avg_attendance, avg_points_game, 'b.')
plt.savefig('plot-attendance-points.png')
plt.clf()

data['margin'] = np.absolute(data['points_game'] - data['opp_points_game'])
avg_margin_game = data.groupby('team_id').mean()['margin']

fit = scipy.stats.linregress(avg_attendance, avg_margin_game)
print('Slope: {}, intercept: {}'.format(fit.slope, fit.intercept))
print('P-value of linregress: {}'.format(fit.pvalue))

fit_line = fit.slope * avg_attendance + fit.intercept

plt.xlabel('Attendance')
plt.ylabel('Win/Loss margin')
plt.plot(avg_attendance, avg_margin_game, 'g.')
plt.plot(avg_attendance, fit_line, 'b-')
plt.savefig('plot-attendance-margin.png')
plt.clf()

residuals = avg_margin_game - fit_line
plt.hist(residuals)
plt.savefig('residuals-hist.png')
plt.clf()

median_attendance = data['attendance'].median()
low_attendance_games = data[data['attendance'] < median_attendance]['margin']
high_attendance_games = data[data['attendance'] >= median_attendance]['margin']

mann_whitney = scipy.stats.mannwhitneyu(low_attendance_games, high_attendance_games)
print('P-value of Mann-Whitney U-test: {}'.format(mann_whitney.pvalue))