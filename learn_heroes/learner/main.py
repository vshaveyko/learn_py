import pdb

#  from collections import defaultdict;

#  data = defaultdict(lambda: defaultdict(lambda: [0, 0], {}), {})

from random_games_data import get_games_data
from teacher import teach_game;

#
# teach in format:
# { ((1,2), (3,4)): { 5: (7, 19} }
# meaning: if picked 1,2 and 3,4 => hero with id 5 has 7/19 chance of winning
#
def teach_it_all():
    for game in get_games_data():
        teach_game(game)

teach_it_all()
