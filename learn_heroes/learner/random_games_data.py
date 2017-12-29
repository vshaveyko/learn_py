import random

def random_team():
    return random.sample(range(1, 113), 10)

def get_games_data(num=1000):
    games = []

    for i in range(0, num):
        teams = random_team()
        won   = set(teams[:5])
        lose  = set(teams[5:])

        games.append({ 'won': won, 'lose': lose })

    return games
