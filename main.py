import os
from neural_net import start
import matches_functions
import file_handling


def setup():
    data_file_name = input(
            'What is the unique filename of the data to train the neural network? (Leave blank if there '
            'is no data) ')
    initials_list = []
    while not os.path.isfile('data/' + data_file_name) and data_file_name != '':
        data_file_name = input(
            'ERROR. What is the unique filename of the data to train the neural network? (Leave blank if there '
            'is no data) ')
    if data_file_name == '':
        number_of_players = 0
        while number_of_players < 4:
            number_of_players = int(input('How many people are playing? (at least 4 players are required) '))
        for i in range(1, number_of_players+1):
            initial = input('Enter a 1 letter unique initial for Player ' + str(i) + ': ')
            while len(initial) != 1 or initial in initials_list:
                initial = input('ERROR. Enter a 1 letter unique initial for Player ' + str(i) + ': ')
            initials_list.append(initial)
        data_file_name = input('What would you like to name the data file? ')
        while os.path.isfile('data/' + data_file_name):
            data_file_name = input('ERROR: FILE ALREADY EXISTS. What would you like to name the data file? ')
        file_handling.new_data(data_file_name, initials_list)
    else:
        initials_list = file_handling.get_initials(data_file_name)
    file_handling.new_championship(data_file_name)
    return data_file_name, initials_list


if __name__ == '__main__':
    count = 0
    data_file = ''
    if not os.path.isdir('championships'):
        os.makedirs('championships', exist_ok=True)
    if not os.path.isdir('data'):
        os.makedirs('data', exist_ok=True)
    if not os.path.isdir('models'):
        os.makedirs('models', exist_ok=True)
    if not os.listdir('championships'):
        data_file, initials = setup()
        matches_functions.start(initials)
    else:
        continue_progress = input('Do you want to continue a previous championship? (y/n) ')
        if continue_progress == 'n':
            data_file, initials = setup()
            matches_functions.start(initials)
        else:
            doc = sorted(os.listdir('championships'))[-1]
            index = doc.index('_')
            data_file = doc[index+1:]
            initials = file_handling.get_initials(data_file)
            matches_functions.start(initials)
            count, info = file_handling.read_values(doc, len(matches_functions.match_codes))
            for row in info:
                matches_functions.update_scores(row[0], row[2], row[1] == 'True', row[3], False)
        start(data_file)
    while True:
        matches_functions.make_match(count)
        count += 1
        print()
