import random

import operator
import pyspark

def random_team():
    return random.sample(range(1, 100), 10)

data = []

for i in range(0, 1000):
    teams = random_team()
    won   = set(teams[:5])
    lose  = set(teams[5:])

    data.append({ 'won': won, 'lose': lose })

team1 = set([1, 2, 3])
team2 = set([6, 7, 21])

def calc_game_weight(game):
    #  print('gameeee', game)

    won = game['won']
    lose = game['lose']

    team1won_len = len(won & team1) + len(lose & team2)
    team2won_len = len(won & team2) + len(lose & team1)

    if (team1won_len == 0 or team2won_len == 0):
        return ('N,A,', 1)

    if team1won_len > team2won_len:
        return ('Team2', team1won_len)
    elif team1won_len < team2won_len:
        return ('Team1', team2won_len)
    else:
        return ('Even', team2won_len)

def main():
    #Intialize a spark context
    with pyspark.SparkContext("local", "PySparkHeroesChances") as sc:
        games = sc.parallelize(data)
        weights = games.map(calc_game_weight)
        counts = weights.reduceByKey(operator.add)

        result = {}

        for word,count in counts.toLocalIterator():
            result[word] = count

        print('result', result)

        print 'team1 win: ', (float(result['Team1']) / (result['Team1'] + result['Team2'] + result['Even']))
        print 'team2 win: ', (float(result['Team2']) / (result['Team1'] + result['Team2'] + result['Even']))
        print 'even: ', (float(result['Even']) / (result['Team1'] + result['Team2'] + result['Even']))

if __name__ == "__main__":
    main()
