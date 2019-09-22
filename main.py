import pickle


class Score:
    def __init__(self, name, seed, number, date, opponent_score, par, used, course, opponent):
        self.name = name
        self.seed = seed
        self.number = number
        self.date = date
        self.opponent_score = opponent_score
        self.par = par
        self.used = used
        self.course = course
        self.opponent = opponent
        self.rel_par = number - par
        if self.rel_par == 0:
            self.rel_par_string = 'E'
        elif self.rel_par > 0:
            self.rel_par_string = '+' + str(self.rel_par)
        else:
            self.rel_par_string = str(self.rel_par)

    def to_string(self):
        return '|{0:5}|{1:15}|{2:<3}|{3:<4}|{4:10}|{5:<5}|{6:4}|{7:4}|'.format(self.date, self.course, self.par, self.seed,
                                                                            self.name, self.number,
                                                                            self.rel_par_string, self.used)

def process_input(choice):
    if choice == 1:
        print_stats()
    elif choice == 2:
        add_match()
    elif choice == 3:
        save_choice = input("Save Changes? (Y/N) ")
        if save_choice == 'y' or save_choice == 'Y':
            write()


def print_stats():
    print("|Date |Course         |Par|Seed|Name      |Score|Rel.|Used|")
    for score in scores:
        print(score.to_string())
    processed_player_names = []
    num_avg_list = []
    rel_avg_list = []
    num_used_list = []
    per_used_list = []
    num_won_list = []
    per_won_list = []
    for identifier_score in scores:
        num_matches = 0
        num_sum = 0
        rel_sum = 0
        num_used = 0
        num_won = 0
        if identifier_score.name not in processed_player_names:
            for score in scores:
                if score.name == identifier_score.name:
                    num_matches += 1
                    num_sum += score.number
                    rel_sum += score.rel_par
                    if score.used == 'Y':
                        num_used += 1
                    if score.number < score.opponent_score:
                        num_won += 1
            processed_player_names.append(identifier_score.name)
            num_avg_list.append(num_sum / num_matches)
            rel_avg_list.append(rel_sum / num_matches)
            num_used_list.append(num_used)
            per_used_list.append(num_used * 100 / num_matches)
            num_won_list.append(num_won)
            per_won_list.append(num_won * 100 / num_matches)
    print('\n|Name      |Num Avg|Rel Avg|Num Used|% Used|Num Won|% Won|')
    i = 0
    while i < len(processed_player_names):
        print('|{0:10}|{1:7}|{2:7}|{3:8}|{4:6}|{5:7}|{6:5}|'.format(processed_player_names[i], num_avg_list[i],
                                                                    rel_avg_list[i], num_used_list[i], per_used_list[i],
                                                                    num_won_list[i], per_won_list[i]))
        i += 1
    print("\n|Date |Course         |Opponent  |Outcome|Score  |Par|Rel. Score|")
    processed_dates = []
    matches = []
    for identifier_score in scores:
        if identifier_score.date not in processed_dates:
            match_scores = []
            for tester_score in scores:
                if tester_score.date == identifier_score.date:
                    match_scores.append(tester_score)
            matches.append(match_scores)
            processed_dates.append(identifier_score.date)
    num_matches = 0
    num_home_matches = 0
    num_away_matches = 0
    num_sum = 0
    rel_sum = 0
    home_sum = 0
    away_sum = 0
    for match_scores in matches:
        num_matches += 1
        num_sum += get_home_score(match_scores)
        rel_sum += get_home_score(match_scores) - match_scores[0].par * 5
        if match_scores[0].course == 'Turtle Creek':
            home_sum += get_home_score(match_scores)
            num_home_matches += 1
        else:
            away_sum += get_home_score(match_scores)
            num_away_matches += 1
        print('|{0:5}|{1:15}|{2:10}|{3:7}|{4:7}|{5:3}| {6:9}|'.format(match_scores[0].date, match_scores[0].course,
                                                                match_scores[0].opponent,
                                                                get_outcome(match_scores),
                                                                str(get_home_score(match_scores)) + '-' +
                                                                str(get_away_score(match_scores)),
                                                                match_scores[0].par * 5,
                                                                get_rel_par_score(match_scores),))
    num_avg = num_sum / num_matches
    rel_avg = rel_sum / num_matches
    if rel_avg > 0:
        rel_avg = '+' + str(rel_avg)
    elif rel_avg == 0:
        rel_avg = 'E'
    home_avg = 'N/A'
    away_avg = 'N/A'
    if num_home_matches > 0:
        home_avg = home_sum / num_home_matches
    if num_away_matches > 0:
        away_avg = away_sum / num_away_matches
    print('\nNumeric Team Average : {}'
          '\nRelative Team Average: {}'
          '\nHome Team Average    : {}'
          '\nAway Team Average    : {}'.format(num_avg, rel_avg, home_avg, away_avg))


def get_rel_par_score(input_match_scores):
    rel_par_value_home = get_home_score(input_match_scores) - input_match_scores[0].par * 5
    rel_par_value_home_string = str(rel_par_value_home)
    if rel_par_value_home > 0:
        rel_par_value_home_string = '+' + str(rel_par_value_home)
    elif rel_par_value_home == 0:
        rel_par_value_home_string = 'E'
    rel_par_value_away = get_away_score(input_match_scores) - input_match_scores[0].par * 5
    rel_par_value_away_string = str(rel_par_value_away)
    if rel_par_value_away > 0:
        rel_par_value_away_string = '+' + str(rel_par_value_away)
    elif rel_par_value_away == 0:
        rel_par_value_away_string = 'E'
    return '{0:3}-{1:3}'.format(rel_par_value_home_string, rel_par_value_away_string)


def get_outcome(input_match_scores):
    wl = get_home_score(input_match_scores) - get_away_score(input_match_scores)
    if wl > 0:
        return "Loss"
    if wl < 0:
        return "Win"
    else:
        tiebreak_outcome = "Tiebreak win or loss? (Enter Win or Loss): "
        return tiebreak_outcome


def get_home_score(input_match_scores):
    numbers = []
    for input_score in input_match_scores:
        numbers.append(input_score.number)
    for i in range(0, 3):
        max = 0
        index = 0
        for j in range(0,8):
            if numbers[j] > max:
                max = numbers[j]
                index = j
        numbers[index] = 0
    sum = 0

    for number in numbers:
        sum += number
    return sum


def get_away_score(input_match_scores):
    numbers = []
    for input_score in input_match_scores:
        numbers.append(input_score.opponent_score)
    for i in range(0, 3):
        max = 0
        index = 0
        for j in range(0,8):
            if numbers[j] > max:
                max = numbers[j]
                index = j
        numbers[index] = 0
    sum = 0

    for number in numbers:
        sum += number

    return sum


def add_match():
    date = input("Date:")
    course = input("Course:")
    par = int(input("Par:"))
    opponent = input('Opponent:')
    for seed in range(1, 9):
        name = input("Name:")
        number = int(input("Score:"))
        opponent_score = int(input("Opponent's Score:"))
        used = input("Used (Y/N):")
        if used == 'y':
            used = 'Y'
        elif used == 'n':
            used = 'N'
        temp_score = Score(name, seed, number, date, opponent_score, par, used, course, opponent)
        scores.append(temp_score)


def write():
    with open('scores.data', 'wb') as file_handle:
        # store the data as binary data stream
        pickle.dump(scores, file_handle)


def read():
    #REEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE
    with open('scores.data', 'rb') as file_handle:
        # read the data as binary data stream
        read_list = pickle.load(file_handle)
    return read_list


choice = 0
scores = read()
#scores = []
#scores.append(Score('Player 1', 1, 34, "10/11", 56, 36, 'Y', 'Turtle Creek', 'OJR'))
#scores.append(Score('Player 2', 2, 35, "10/11", 56, 36, 'Y', 'Turtle Creek', 'OJR'))
#scores.append(Score('Player 3', 3, 36, "10/11", 56, 36, 'Y', 'Turtle Creek', 'OJR'))
#scores.append(Score('Player 4', 4, 37, "10/11", 56, 36, 'Y', 'Turtle Creek', 'OJR'))
#scores.append(Score('Player 5', 5, 38, "10/11", 56, 36, 'Y', 'Turtle Creek', 'OJR'))
#scores.append(Score('Player 6', 6, 39, "10/11", 56, 36, 'N', 'Turtle Creek', 'OJR'))
#scores.append(Score('Player 7', 7, 40, "10/11", 56, 36, 'N', 'Turtle Creek', 'OJR'))
#scores.append(Score('Player 8', 8, 41, "10/11", 56, 36, 'N', 'Turtle Creek', 'OJR'))
#scores.append(Score('Player 1', 1, 35, "10/12", 56, 36, 'Y', 'Turtle Creek', 'PV'))
#scores.append(Score('Player 2', 2, 36, "10/12", 56, 36, 'Y', 'Turtle Creek', 'PV'))
#scores.append(Score('Player 3', 3, 37, "10/12", 56, 36, 'Y', 'Turtle Creek', 'PV'))
#scores.append(Score('Player 4', 4, 38, "10/12", 56, 36, 'Y', 'Turtle Creek', 'PV'))
#scores.append(Score('Player 5', 5, 39, "10/12", 56, 36, 'Y', 'Turtle Creek', 'PV'))
#scores.append(Score('Player 6', 6, 40, "10/12", 56, 36, 'N', 'Turtle Creek', 'PV'))
#scores.append(Score('Player 7', 7, 41, "10/12", 56, 36, 'N', 'Turtle Creek', 'PV'))
#scores.append(Score('Player 8', 8, 42, "10/12", 56, 36, 'N', 'Turtle Creek', 'PV'))

while choice != 3:
    print("\n1. See Stats\n2. Add Match\n3. Quit")
    choice = int(input(">"))
    process_input(choice)