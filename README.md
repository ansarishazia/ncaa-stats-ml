# Introduction
This report outlines and analyzes data science techniques like statistical tests and machine learning, performed on official NCAA Men’s Basketball data obtained through Kaggle. Each section explores a different relationship between the data, justifying the use of each technique and explaining the findings. This report can aid studies in sports science and coaching as well as form a basis for further research.

# The data
**Dataset: [https://www.kaggle.com/ncaa/ncaa-basketball](https://www.kaggle.com/ncaa/ncaa-basketball)**

The data exists in the form of multiple tables, with game stats, team-information stats and individual player-level stats available in separately, making querying easier. The challenge however is in consolidating historical data that exists separately and is missing certain stats that modern data has such as FG%, 3PT%, fouls, etc. To narrow statistical inference to modern college basketball, only data from 2007 to 2017 is considered.

# Querying the data  

The datasets offered through Kaggle are hosted on Google Cloud Platform, and are available through Google’s BigQuery service. BQ provides a simple to use Python client but requires authentication credentials. Follow [https://cloud.google.com/docs/authentication/getting-started](https://cloud.google.com/docs/authentication/getting-started) to obtain a credentials JSON and set the GOOGLE_APPLICATION_CREDENTIALS environment variable to point to this file. BQ offers the use of SQL style queries for easy querying of data from the table. This is leveraged by the script ‘pull-ncaa-stats.py’ to query all tables needed for this project and write them to a .csv file (as cache).

# Cleaning the data
This phase of the pipeline required two steps. To standardize the date format used, and consolidate historical data with modern data. In ‘clean-data.py’, Pandas’ read_csv function allows parsing dates through the ‘parse_dates’ keyword argument which automatically takes care of all different data formats used. The script reads both the CSVs for historical as well as modern data and concatenates them using only the common columns. As there is an overlap in seasons, drop_duplicates() is called to remove any games that are counted twice, once from each file. One this data is consolidated it is written back to 'ncaa_consolidated_07_to_17.csv'. Dropping rows with NaN, or null values with dropna() is done when needed before any model or test is performed.

# Study 1: Game attendance and game performance  

This section explores the relationship between a game’s attendance, and how well each team playing performs. It is easy to think that teams with higher attendances usually produce high scoring games, however ‘attendance-performance.py’ takes a statistical approach to ask the question if a team’s average attendance affects how many points they score a game.

 ## Linear Regression
 
The script reads in the consolidated csv file to a Pandas dataframe. Then we group by the ‘team-id’ column and aggregate using mean(). This gives average attendance and points scored per team. Plotting this we get the following graph.

![](https://i.imgur.com/nbBh30x.png)

However, points per game does not tell the entire story. Since we are missing data that shows which team is at home, we must rephrase the question to determine performance. Instead of plotting against average points per game, we look at the win/loss margin. This metric shows how well both teams performed relative to each other. A higher margin shows high disparity in the performance of teams whereas a lower margin shows a close game where both teams were equal.

We plot against average win/loss margin instead.
![](https://i.imgur.com/6dsuEtm.png)

Regression is performed through scipy.stats.linregress and the line of best fit shows a negative relationship, suggesting that higher attendances pressure teams into tighter games. The p-value obtained is 0.004141598225944108, meaning we can reject the null hypothesis at a significance level of 0.05. But does a linear regression work here? We have made the assumption here that our data is normally distributed, however, on the plot it does not appear so. Let’s take a look at the residuals distribution calculated by average_margin - line_of_fit.

![enter image description here](https://i.imgur.com/RUhx89h.png)

## Mann-Whitney U-test

It is evident from the histogram that the residuals are not normally distributed and our assumption fails. Perhaps, we can reshape the question to a more appropriate statistical tests that does not assume any distribution of data, like the Mann-Whitney U-test. Instead of having attendance be continuous we can interpret it as low, and high. By finding the median attendance we split the win/loss margin to obtain two series, high attendance margins and low attendance margins. Now we can apply the Mann-Whitney U-test and we obtain significant p-value of 6.813588181013765e-83 showing that there does exist a difference in the samples from the two groups.

Now that we are able to prove a relationship between attendance and team performance, can we predict the attendance in a team’s upcoming game given their previous game’s attendance and performance?

Refer to the script 'predict-attendance.py' for code related to this part.

## Gaussian Naive Bayesian Classifier

First instinct is to apply GaussianNB classifier to the problem. However, the problem is that we cannot predict a number, instead only a category. So we simplify the problem. We predict whether attendance in the next game goes up or down. Now we have transformed the problem into a classification application and can apply different classifiers.

Load the CSV file into a Pandas DataFrame and sort by ‘team_id’ and then ‘scheduled_date’. Create another DataFrame from this DataFrame that has ‘team_id’ and ‘attendance’ but shift this by 1 row. Join the first DataFrame with this one on ‘team_id’ so that each row has current attendance, points, opponent points, margin, and win along with the next played game’s attendance. Now, remove any null with dropna() and create a column where attendance difference is classified as ‘UP’ and ‘DOWN’. Also transform boolean values in the ‘win’ column to 1 or 0.

The chosen features include ‘attendance’, ‘points’, ‘win’ and ‘margin’. Applying GaussianNB with StandardScalar provides unsatisfactory results with scores:

GaussianNB training score: 0.5764116575591985

GaussianNB validation score: 0.5770881213738127

This is a failure of the classifier as we have made false assumptions and we already know the data does not have a normal distribution. So let’s try a decision tree.  

## Decision Tree Classifier

We keep the same DataFrame and just apply DecisionTreeClassifier with 17 as the max_depth. Results are a little better:

Decision Tree training score: 0.6969838208507446

Decision Tree validation score: 0.609938766654345

Tweaking max_depth to be higher overfits and provides worse a validation score. We can conclude that Decision Tree also fails to provide acceptable scores. One of the reasons for this is that we do not have data that shows which team is at their home venue and so an underlying assumption is that attendance at each game is played at neutral grounds with neutral supporters. This is one of the flaws of this prediction. Taking into account home grounds as well as data from the past 5 games instead of just the previous game can greatly improve the results.