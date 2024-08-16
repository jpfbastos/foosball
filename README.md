# Foosball Championship Manager #

## General Information

This is a program which creates and manages foosball championships. It displays match information along with championship results, and has the ability to store progress by saving the championship information in .csv files. Moreover, it also uses Scikit-learn's Multi-layer Perceptron (MLP) Regressor which, based on previous information about the teams and their results, tries to predict the result of the upcoming match.

The purpose of this solution is so there is a way to store the results of matches in an organised way which can then be structured into championships to create a more competitive edge amongst the players. 

I usually play foosball with my family during the summer, so this was a fun way to have an organised way to determine who the best player or player pair is, and to learn more about reading/writing data and processing it, along with an introduction to MLP Regressors and simple neural networks.

## Technologies Used

- Python version 3.9
- Pandas version 2.2
- Numpy version 1.24
- Scikit-learn version 1.4

## Features

- Stores progress using csv files, making it easy to stop and re-start a championship.
- Displays updated leaderboard so the players know who is ahead
- Uses previous data and MLP Regressor to predict the outcome of upcoming matches

## Screenshots

## Project Status
In progress

## Next Steps

- Player leaderboard in order as well
- Produce final results table on both csv file (done) and terminal (to-do)
- Ability to modify championship length or type (only include closest matches)
- Ability to modify length of matches
- Include case where there is no previous data
