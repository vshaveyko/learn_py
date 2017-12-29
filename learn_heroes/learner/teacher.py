from orm import add_hero_stat_for_matchup, find_or_create_matchup

import pdb

import itertools

def learn(team1, team2, team_heroes, is_win):
    matchup_id = find_or_create_matchup(team1, team2)

    for hero_id in team_heroes:
        add_hero_stat_for_matchup(matchup_id, hero_id, is_win=is_win)

def learn_loss(team1, team2, team_heroes):
    learn(team1, team2, team_heroes, is_win=False)

def learn_win(team1, team2, team_heroes):
    learn(team1, team2, team_heroes, is_win=True)

def teach_game(game):
    won  = game['won']
    lose = game['lose']

    won_combinations  = [()]
    lose_combinations = [()]

    #  for i in range(1, 4):
    i = 1

    won_combinations  += list(itertools.combinations(won, i))
    lose_combinations += list(itertools.combinations(lose, i))

    combs = []

    for won_comb in won_combinations:
        for lose_comb in lose_combinations:
            combs.append((won_comb, lose_comb))

    for win, loss in combs:
        learn_win(win, loss,  won - set(win))
        learn_loss(loss, win, lose - set(loss))
