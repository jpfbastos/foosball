import os
import neural_net
import matches_functions
import file_handling

if __name__ == '__main__':
    neural_net.start()
    count = 0
    if not os.listdir('championships'):
        file_handling.new_championship()
    else:
        continue_progress = input('Do you want to continue a previous championship? (y/n) ')
        if continue_progress == 'n':
            file_handling.new_championship()
        else:
            count, info = file_handling.read_values('championships/' + sorted(os.listdir('championships'))[-1],
                                                    len(matches_functions.make_match_codes()))
            for row in info:
                matches_functions.update_scores(row[0], row[2], row[1] == 'True', row[3], False)
    while True:
        matches_functions.make_match(count)
        count += 1
        print()
