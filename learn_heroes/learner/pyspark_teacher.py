import pyspark

def preprocess(games):
    return games

from collections import defaultdict;
import itertools;

from merge import merge_dicts

from psycopg2.extras import execute_batch
import psycopg2
def get_team_combiations(won, lose):
    won_combinations  = [()]
    lose_combinations = [()]

    for i in range(1, 3):
        won_combinations  += list(itertools.combinations(won, i))
        lose_combinations += list(itertools.combinations(lose, i))

    combs = []

    for won_comb in won_combinations:
        for lose_comb in lose_combinations:
            combs.append((won_comb, lose_comb))

    return combs

def aggregatorSeqOp(accumulator, game):
    won  = game['won']
    lose = game['lose']

    for win, loss in get_team_combiations(won, lose):
        if (win, loss) not in accumulator:
            accumulator[(win, loss)] = {}

        if (loss, win) not in accumulator:
            accumulator[(loss, win)] = {}

        winning = accumulator[(win, loss)]

        for hero_id in won - set(win):
            if hero_id not in winning:
                winning[hero_id] = [0, 0]

            winning[hero_id][0] += 1
            winning[hero_id][1] += 1

        losing = accumulator[(loss, win)]

        for hero_id in lose - set(loss):
            if hero_id not in losing:
                losing[hero_id] = [0, 0]

            losing[hero_id][1] += 1

    return accumulator

def merge_results(left, right):
    return [left[0] + right[0], left[1] + right[1]]

def aggregatorCombOp(accumulator_left, accumulator_right):
    return merge_dicts(accumulator_left, accumulator_right, merge_results)

from orm import generate_hero_stats_upsert_statement;

import pdb;

def teach_games(games):
    preprocessed = preprocess(games)

    with pyspark.SparkContext("local", "PySparkHeroesData") as sc:
        spark_games = sc.parallelize(preprocessed)

        def _inner(partition):
            items = list(partition)
            #  print( item, partition )

            pg_conn = psycopg2.connect(dbname='learn_heroes_view_development')

            for item in items:
                statement = generate_hero_stats_upsert_statement(item[0])
                variables = { 'hero_ids': [], 'num_wins': [], 'num_loss': [] }

                for k,v in item[1].items():
                    variables['hero_ids'].append(k)
                    variables['num_wins'].append(v[0])
                    variables['num_loss'].append(v[1])

                with pg_conn:
                      with pg_conn.cursor() as cur:
                          execute_batch(cur, statement, [variables])
                      yield True

        aggregated = spark_games.aggregate(
                {},
                aggregatorSeqOp,
                aggregatorCombOp
            )

        sc.parallelize(aggregated.items(), 100).mapPartitions(_inner).collect()

from random_games_data import get_games_data

teach_games(get_games_data())
