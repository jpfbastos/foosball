import pickle
import os.path
import pandas as pd
from sklearn.neural_network import MLPRegressor
from sklearn.model_selection import train_test_split


def is_trained(model):
    try:
        _ = model.coefs_
        return True
    except AttributeError:
        return False


def start(data_file_name):
    global data_file_path, model_file_path, df, initials, regr
    data_file_path = 'data/' + data_file_name
    model_file_path = 'models/' + data_file_path[5:-4] + '.pkl'
    df = pd.read_csv(data_file_path)
    initials = list(df)[:-1]

    if os.path.isfile(model_file_path):
        with open(model_file_path, 'rb') as f:
            regr = pickle.load(f)
    else:
        regr = MLPRegressor(hidden_layer_sizes=(50,), activation='relu', max_iter=300, warm_start=True)

        if not df.empty:
            X, y = df.iloc[:, :-1], (
                    df.iloc[:, -1:].values / 6).ravel()  # max number of goals as output is between -1 and 1
            X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.8, test_size=0.2)

            regr.fit(X_train, y_train)


def save():
    global regr
    with open(model_file_path, 'wb') as f:
        pickle.dump(regr, f)


def predict(game_code, is_home):
    global regr

    if not is_trained(regr):
        return None

    player_dict = {initial: 0 for initial in initials}
    if is_home:
        player_dict.update({game_code[0]: 1, game_code[1]: 1, game_code[2]: -1, game_code[3]: -1})
    else:
        player_dict.update({game_code[0]: -1, game_code[1]: -1, game_code[2]: 1, game_code[3]: 1})

    input_data = pd.DataFrame([player_dict])

    prediction = regr.predict(input_data)

    expected_gd = round(prediction[0] * 6, 1)  # output is between -1 and 1, and we need it to be between -6 and 6
    return expected_gd


def improve(game_code, is_home, goal_difference):
    global regr
    player_dict = {initial: 0 for initial in initials}
    if is_home:
        player_dict.update({game_code[0]: 1, game_code[1]: 1, game_code[2]: -1, game_code[3]: -1})
    else:
        player_dict.update({game_code[0]: -1, game_code[1]: -1, game_code[2]: 1, game_code[3]: 1})

    input_data = pd.DataFrame([player_dict])

    regr.fit(input_data, [goal_difference / 6])

    new_data = input_data.assign(GD=goal_difference)
    if os.path.isfile(data_file_path):
        new_data.to_csv(data_file_path, mode='a', index=False, header=False)
    else:
        new_data.to_csv(data_file_path, mode='w', index=False)


data_file_path = ''
model_file_path = 'models/' + data_file_path[5:-4] + '.pkl'
df = pd.DataFrame()
initials = []
regr = MLPRegressor()
