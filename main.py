import os
from neural_net import start
import matches_functions
import file_handling


def get_data():
    data_file_name = input(
            'What is the filename of where the data to train the neural network? (Leave blank if there '
            'is no data) ')
    while not os.path.isfile('data/' + data_file_name) and data_file_name != '':
        data_file_name = input(
            'ERROR. What is the filename of where the data to train the neural network? (Leave blank if there '
            'is no data) ')
    if data_file_name == '':
        initials_list = []
        number_of_players = int(input("How many people are playing? (at least 4 players are required) "))
        for i in range(1, number_of_players+1):
            initial = input("Enter a 1 letter unique initial for Player " + str(i) + ": ")
            while len(initial) != 1 or initial in initials_list:
                initial = input("ERROR. Enter a 1 letter unique initial for Player " + str(i) + ": ")
            initials_list.append(initial)
    return 'data/' + data_file_name, initials_list


if __name__ == '__main__':
    count = 0
    if not os.path.isdir('championships'):
        os.makedirs('championships', exist_ok=True)
    if not os.listdir('championships'):
        file_handling.new_championship()
    else:
        continue_progress = input('Do you want to continue a previous championship? (y/n) ')
        if continue_progress == 'n':
            data_file, initials = get_data()
            start(data_file)
            file_handling.new_championship()
            matches_functions.make_names()
        else:
            data_file = 'championships/' + sorted(os.listdir('championships'))[-1]
            count, info = file_handling.read_values(data_file, len(matches_functions.make_match_codes()))
            start(data_file)
            for row in info:
                matches_functions.update_scores(row[0], row[2], row[1] == 'True', row[3], False)
    while True:
        matches_functions.make_match(count)
        count += 1
        print()
