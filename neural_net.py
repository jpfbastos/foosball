import pickle
import os.path
import pandas as pd
from sklearn.neural_network import MLPRegressor
from sklearn.model_selection import train_test_split

clf = MLPRegressor()

model_file_path = 'model.pkl'
data_file_path = 'data/matrecos.csv'


def start():
    global clf
    if os.path.isfile(model_file_path):
        with open(model_file_path, 'rb') as f:
            clf = pickle.load(f)
    else:
        df = pd.read_csv(data_file_path)

        X, y = df.iloc[:, :-1], (
                    df.iloc[:, -1:].values / 6).ravel()  # max number of goals as output is between -1 and 1
        X_train, X_test, y_train, y_test = train_test_split((X, y), left_side=0.8)

        clf = MLPRegressor(hidden_layer_sizes=(10,), activation='relu', max_iter=300, warm_start=True, verbose=False)
        clf.fit(X_train, y_train)


def save():
    global clf
    with open(model_file_path, 'wb') as f:
        pickle.dump(clf, f)


def predict(initials, game_code, is_home):
    global clf
    player_dict = {initial: 0 for initial in initials}
    if is_home:
        player_dict.update({game_code[0]: 1, game_code[1]: 1, game_code[2]: -1, game_code[3]: -1})
    else:
        player_dict.update({game_code[0]: -1, game_code[1]: -1, game_code[2]: 1, game_code[3]: 1})

    input_data = pd.DataFrame([player_dict])

    prediction = clf.predict(input_data)
    expected_gd = round(prediction[0] * 6, 1)  # output is between -1 and 1: we need it to be between -6 and 6
    return expected_gd


def improve(initials, game_code, is_home, goal_difference):
    global clf

    player_dict = {initial: 0 for initial in initials}
    if is_home:
        player_dict.update({game_code[0]: 1, game_code[1]: 1, game_code[2]: -1, game_code[3]: -1})
    else:
        player_dict.update({game_code[0]: -1, game_code[1]: -1, game_code[2]: 1, game_code[3]: 1})

    input_data = pd.DataFrame([player_dict])

    clf.fit(input_data, [goal_difference / 6])

    new_data = input_data.assign(GD=goal_difference)
    if os.path.isfile(data_file_path):
        new_data.to_csv(data_file_path, mode='a', index=False, header=False)
    else:
        new_data.to_csv(data_file_path, mode='w', index=False)
