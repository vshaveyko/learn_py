import random

def random_team():
    return random.sample(range(1, 100), 10)

def generate_games(num=1000):
    games = []

    for i in range(0, num):
        teams = random_team()
        won   = set(teams[:5])
        lose  = set(teams[5:])

        games.append({ 'won': won, 'lose': lose })

    return games

import itertools
import pdb

from collections import defaultdict;

data = defaultdict(lambda: defaultdict(lambda: [0, 0], {}), {})

def win_learner(target):
    target[0] += 1
    target[1] += 1

def learn_win(comb, team_heroes):
    for hero_id in team_heroes:
        win_learner(data[comb][hero_id])

def loss_learner(target):
    target[1] += 1

def learn_loss(comb, team_heroes):
    for hero_id in team_heroes:
        loss_learner(data[comb][hero_id])

def teach_game(game):
    won  = game['won']
    lose = game['lose']

    won_combinations  = [()]
    lose_combinations = [()]

    for i in range(1, 6):
        won_combinations  += list(itertools.combinations(won, i))
        lose_combinations += list(itertools.combinations(lose, i))

    for won_comb in won_combinations:
        for lose_comb in lose_combinations:
            combs.append((won_comb, lose_comb))

    for win, loss in combs:
        learn_win((win, loss),  won - set(win))
        learn_loss((loss, win), lose - set(loss))

#
# teach in format:
# { ((1,2), (3,4)): { 5: (7, 19} }
# meaning: if picked 1,2 and 3,4 => hero with id 5 has 7/19 chance of winning
#
def teach_it_all():
    for game in generate_games():
        teach_game(game)

def predict_best_pick(team1, team2):
    return map(lambda v: v[0], sorted(data[(team1, team2)].items(), key=lambda x: x[1][0] / x[1][1]))

def calc_win_probability(team1, team2):
    def reducer(output, current):
        print 'outp', output, 'curr', current

        return [output[0] + current[0], output[1] + current[1]]

    match_up_data = data[(team1, team2)]

    if match_up_data:
        reduced = reduce(reducer, match_up_data.values(), [0, 0])

        return reduced[0] / reduced[1]
    else:
        raise BaseException
