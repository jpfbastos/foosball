import pandas as pd
import os

HEADER = ["game_code", "is_home", "home", "away", "score", "goal_difference", "expected_gd", "error"]


def update_csv(updates):
    docs = sorted(os.listdir('championships'))
    filename = 'championships/' + docs[-1]
    data = {HEADER[i]: updates[i] for i in range(len(updates))}
    df = pd.DataFrame(data, index=[0])
    df.to_csv(filename, mode='a', index=False, header=False)


def new_championship():
    df = pd.DataFrame(columns=HEADER)
    docs = sorted(os.listdir('championships'))
    if not os.listdir('championships'):
        df.to_csv('championships/championship00.csv', index=False)
    else:
        df.to_csv('championships/championship' + str(int(docs[-1][12:-4]) + 1).zfill(2) + '.csv', index=False)


def read_values(csv_file, max_matches):
    info = []
    data = pd.read_csv(csv_file)
    count = len(data) - 1  # title does not count
    if count > max_matches:
        confirmation = input('All games have been completed - do you want to play another championship? (y/n) ')
        if confirmation == 'n':
            exit()
        else:
            new_championship()
            count = 0
    else:
        for row in data.values:
            info.append([row[0], row[1], row[4], row[7]])  # code, isHome, result, expected_gd
    return count, info
