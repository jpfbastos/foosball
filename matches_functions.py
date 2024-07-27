import file_handling
import neural_net
from random import randint
from random import getrandbits


def make_names(initials):
    names = {}
    for initial in initials:
        name = input("What name would you like displayed for the initial " + initial + "? (Leave blank if " + initial +
                     "is not playing) ")
        name = ''.join(name.split())
        if name != '':
            names.update({initial: name})
    return names


def make_pairs():
    pairs = []
    for i in range(len(names) - 1):
        for j in range(i + 1, len(names)):
            pairs.append(list(names.keys())[i] + list(names.keys())[j])
    return pairs


def make_match_codes():
    matches = []
    for i in range(len(pairs) - 1):
        first_pair = pairs[i]
        for j in range(i + 1, len(pairs)):
            second_pair = pairs[j]
            if second_pair.find(first_pair[0]) == -1 \
                    and second_pair.find(first_pair[1]) == -1:
                matches.append(first_pair + second_pair)
    return matches


def make_matches_dict():
    has_been_played = {}
    for match in match_codes:
        has_been_played.update({match: False})
    return has_been_played


def start(initials):
    global names, pairs, match_codes, scores, pairs_scores, played_matches
    print(initials)
    names = make_names(initials)
    print(names)
    pairs = make_pairs()
    print(pairs)
    match_codes = make_match_codes()
    print(match_codes)
    scores = dict(zip(list(names.keys()), [0] * len(names)))
    pairs_scores = dict(zip(pairs, [0] * len(pairs)))

    played_matches = make_matches_dict()


def select_match(matches_played):
    matches_filtered = [key for key, value in matches_played.items() if not value]
    match = matches_filtered[randint(0, len(matches_filtered) - 1)]
    is_home = bool(getrandbits(1))
    if is_home:
        print(names.get(match[0]) + '/', end='')
        print(names.get(match[1]) + ' - ', end='')
        print(names.get(match[2]) + '/', end='')
        print(names.get(match[3]))
    else:
        print(names.get(match[2]) + '/', end='')
        print(names.get(match[3]) + ' - ', end='')
        print(names.get(match[0]) + '/', end='')
        print(names.get(match[1]))
    return match, is_home


def print_scores():
    for initial in scores:
        if scores.get(initial) == 1:
            print(names.get(initial), 'has', scores.get(initial), 'win')
        else:
            print(names.get(initial), 'has', scores.get(initial), 'wins')
    print()
    sorted_dict = {k: v for k, v in sorted(pairs_scores.items(), key=lambda item: item[1], reverse=True)}
    sorted_dict = dict(list(sorted_dict.items())[0: 3])
    for item in sorted_dict.items():
        if scores.get(initial) == 1:
            print(names.get(item[0][0]) + '/' + names.get(item[0][1]), 'has', item[1], 'win')
        else:
            print(names.get(item[0][0]) + '/' + names.get(item[0][1]), 'has', item[1], 'wins')
    print("------------")
    print()


def update_scores(code, score, is_home, expected_gd, writing_to_csv=True):
    goal_difference = int(score[0]) - int(score[2])
    error = round(goal_difference - expected_gd, 1)
    if is_home:
        if score[0] < score[2]:
            scores.update({code[2]: scores.get(code[2]) + 1, code[3]: scores.get(code[3]) + 1})
            pairs_scores.update({code[2:]: pairs_scores.get(code[2:]) + 1})
        else:
            scores.update({code[0]: scores.get(code[0]) + 1, code[1]: scores.get(code[1]) + 1})
            pairs_scores.update({code[:2]: pairs_scores.get(code[:2]) + 1})
    else:
        if score[2] < score[0]:
            scores.update({code[2]: scores.get(code[2]) + 1, code[3]: scores.get(code[3]) + 1})
            pairs_scores.update({code[2:]: pairs_scores.get(code[2:]) + 1})
        else:
            scores.update({code[0]: scores.get(code[0]) + 1, code[1]: scores.get(code[1]) + 1})
            pairs_scores.update({code[:2]: pairs_scores.get(code[:2]) + 1})
    updates = [code, is_home, names.get(code[2]) + '/' + names.get(code[3]),
               names.get(code[0]) + '/' + names.get(code[1]), score, goal_difference, expected_gd, error]
    if writing_to_csv:
        file_handling.update_csv(updates)
    print_scores()


def update_scores_and_nn(code, score, is_home, expected_gd):
    update_scores(code, score, is_home, expected_gd)
    goal_difference = int(score[0]) - int(score[2])
    neural_net.improve(code, is_home, goal_difference)


def is_championship_over(count):
    return (count + 1) % len(match_codes) == 0


def write_final_results_csv():
    file_handling.update_csv(["--------------"])
    file_handling.update_csv(["Wins"])
    sorted_scores = {k: v for k, v in sorted(scores.items(), reverse=True, key=lambda item: item[1])}
    for item in sorted_scores.items():
        file_handling.update_csv([names.get(item[0]), item[1]])
    file_handling.update_csv(["--------------"])
    file_handling.update_csv(["Pair Wins"])
    sorted_scores = {k: v for k, v in sorted(pairs_scores.items(), reverse=True, key=lambda item: item[1])}
    for item in sorted_scores.items():
        key = names.get(item[0][0]) + '/' + names.get(item[0][1])
        file_handling.update_csv([key, item[1]])


def begin_new_championship():
    global scores
    global pairs_scores
    global played_matches

    file_handling.new_championship()
    scores = scores.fromkeys(scores, 0)
    pairs_scores = pairs_scores.fromkeys(pairs_scores, 0)
    played_matches = played_matches.fromkeys(played_matches, 0)


def make_match(count):
    global played_matches, match_codes
    print(match_codes)
    match_number = count % len(match_codes) + 1
    print("Match", match_number, "/", len(match_codes))
    code, is_home = select_match(played_matches)
    played_matches.update({code: True})
    expected_gd = neural_net.predict(code, is_home)
    print("xGD:", expected_gd)
    score = input("What was the score? ")
    print()
    update_scores_and_nn(code, score, is_home, expected_gd)

    if is_championship_over(count):
        write_final_results_csv()
        confirmation = input('All games have been completed - do you want to play another championship? (y/n) ')
        if confirmation == 'n':
            print_scores()
            neural_net.save()
            exit()
        else:
            begin_new_championship()
    else:
        keep_playing = input('Do you want to keep playing? (y/n) ')
        if keep_playing == 'n':
            print_scores()
            neural_net.save()
            exit()


names = {}

pairs = []
match_codes = []

scores = {}
pairs_scores = {}

played_matches = {}

'''match code (ABCD), home (Adam/Ben), away (Adam/Ben), goal difference (float),
 actual goal difference (float), error (float)'''
