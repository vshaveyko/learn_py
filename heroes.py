import random

import operator
import pyspark

def random_team():
    return random.sample(range(1, 100), 10)

data = []

for i in range(0, 1000000):
    teams = random_team()
    won   = set(teams[:5])
    lose  = set(teams[5:])

    data.append({ 'won': won, 'lose': lose })

team1 = set([1,2,3])
team2 = set([6,7])

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
        return ('Even', 1)

def main():
    #Intialize a spark context
    with pyspark.SparkContext("local", "PySparkHeroesChances") as sc:
        #Get a RDD containing lines from this script file
        games = sc.parallelize(data)
        #Split each line into words and assign a frequency of 1 to each word
        weights = games.map(calc_game_weight)
        #count the frequency for words
        counts = weights.reduceByKey(operator.add)

        #Sort the counts in descending order based on the word frequency
        #Get an iterator over the counts to print a word and its frequency
        result = {}

        for word,count in counts.toLocalIterator():
            result[word] = count

        print('result', result)

        print 'team1 win: ', (float(result['Team1']) / (result['Team1'] + result['Team2'] + result['Even']))
        print 'team2 win: ', (float(result['Team2']) / (result['Team1'] + result['Team2'] + result['Even']))
        print 'even: ', (float(result['Even']) / (result['Team1'] + result['Team2'] + result['Even']))

if __name__ == "__main__":
    main()
