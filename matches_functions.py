import file_handling
import neural_net
from random import randint
from random import getrandbits


def make_pairs():
    pairs = []
    for i in range(len(INITIALS) - 1):
        for j in range(i + 1, len(INITIALS)):
            pairs.append(INITIALS[i] + INITIALS[j])
    return pairs


def make_match_codes():
    matches = []
    for i in range(len(PAIRS) - 1):
        first_pair = PAIRS[i]
        for j in range(i + 1, len(PAIRS)):
            second_pair = PAIRS[j]
            if second_pair.find(first_pair[0]) == -1 \
                    and second_pair.find(first_pair[1]) == -1:
                matches.append(first_pair + second_pair)
    return matches


def make_matches_dict():
    has_been_played = {}
    for match in MATCH_CODES:
        has_been_played.update({match: False})
    return has_been_played


def select_match(matches_played):
    matches_filtered = [key for key, value in matches_played.items() if not value]
    match = matches_filtered[randint(0, len(matches_filtered) - 1)]
    is_home = bool(getrandbits(1))
    if is_home:
        print(NAMES.get(match[0]) + '/', end='')
        print(NAMES.get(match[1]) + ' - ', end='')
        print(NAMES.get(match[2]) + '/', end='')
        print(NAMES.get(match[3]))
    else:
        print(NAMES.get(match[2]) + '/', end='')
        print(NAMES.get(match[3]) + ' - ', end='')
        print(NAMES.get(match[0]) + '/', end='')
        print(NAMES.get(match[1]))
    return match, is_home


def print_scores():
    for initial in scores:
        if scores.get(initial) == 1:
            print(NAMES.get(initial), 'has', scores.get(initial), 'win')
        else:
            print(NAMES.get(initial), 'has', scores.get(initial), 'wins')
    print()
    sorted_dict = {k: v for k, v in sorted(pairs_scores.items(), key=lambda item: item[1], reverse=True)}
    sorted_dict = dict(list(sorted_dict.items())[0: 3])
    for item in sorted_dict.items():
        if scores.get(initial) == 1:
            print(NAMES.get(item[0][0]) + '/' + NAMES.get(item[0][1]), 'has', item[1], 'win')
        else:
            print(NAMES.get(item[0][0]) + '/' + NAMES.get(item[0][1]), 'has', item[1], 'wins')
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
    updates = [code, is_home, NAMES.get(code[2]) + '/' + NAMES.get(code[3]),
               NAMES.get(code[0]) + '/' + NAMES.get(code[1]), score, goal_difference, expected_gd, error]
    if writing_to_csv:
        file_handling.update_csv(updates)
    print_scores()


def update_scores_and_nn(code, score, is_home, expected_gd):
    update_scores(code, score, is_home, expected_gd)
    goal_difference = int(score[0]) - int(score[2])
    neural_net.improve(NAMES.keys(), code, is_home, goal_difference)


def is_championship_over(match_number, count):
    return match_number % (len(MATCH_CODES)) == 0 and count != 0


def write_final_results_csv():
    file_handling.update_csv(["--------------", "Wins"])
    sorted_scores = {k: v for k, v in sorted(scores.items(), reverse=True, key=lambda item: item[1])}
    for item in sorted_scores.items():
        file_handling.update_csv([NAMES.get(item[0]), item[1]])
    file_handling.update_csv(["--------------", "Pair Wins"])
    sorted_scores = {k: v for k, v in sorted(pairs_scores.items(), reverse=True, key=lambda item: item[1])}
    for item in sorted_scores.items():
        key = NAMES.get(item[0][0]) + '/' + NAMES.get(item[0][1])
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
    global played_matches

    match_number = count % len(MATCH_CODES) + 1
    print("Match", match_number, "/", len(MATCH_CODES))
    code, is_home = select_match(played_matches)
    played_matches.update({code: True})
    expected_gd = neural_net.predict(NAMES.keys(), code, is_home)
    print("xGD:", expected_gd)
    score = input("What was the score? ")
    update_scores_and_nn(code, score, is_home, expected_gd)
    print()
    print()

    if is_championship_over(match_number, count):
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


INITIALS = ['J', 'G', 'K', 'V', 'D', 'M']
NAMES = {'J': 'JP', 'G': 'Gucas', 'K': 'Kikas', 'V': 'Vu', 'D': 'Daddy', 'M': 'Mummy'}

PAIRS = make_pairs()
MATCH_CODES = make_match_codes()

scores = dict(zip(INITIALS, [0] * len(INITIALS)))
pairs_scores = dict(zip(PAIRS, [0] * len(PAIRS)))

played_matches = make_matches_dict()

''' match code (ABCD), home (Adam/Ben), away (Adam/Ben), goal difference (float),
 actual goal difference (float), error (float)'''
