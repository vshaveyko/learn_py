def predict_best_pick(team1, team2):
    return map(lambda v: v[0], sorted(data[(team1, team2)].items(), key=lambda x: x[1][0] / x[1][1]))

def calc_win_probability(team1, team2):
    def reducer(output, current):
        return [output[0] + current[0], output[1] + current[1]]

    match_up_data = data[(team1, team2)]

    if match_up_data:
        reduced = reduce(reducer, match_up_data.values(), [0, 0])

        return reduced[0] / reduced[1]
    else:
        raise BaseException
