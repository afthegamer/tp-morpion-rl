from collections import defaultdict

from learning import (opponent_next, opponent_random, play_game, play_opponents,
                      pourcentages)


def valeur_initiale():
    return 0.5


if __name__ == "__main__":
    parties = 10000
    print("random (X) vs random (O)  :", pourcentages(play_opponents(opponent_random, opponent_random) for _ in range(parties)))
    print("next   (X) vs random (O)  :", pourcentages(play_opponents(opponent_next, opponent_random) for _ in range(parties)))
    print("random (X) vs next   (O)  :", pourcentages(play_opponents(opponent_random, opponent_next) for _ in range(parties)))
    values = defaultdict(valeur_initiale)
    print("greedy (X) vs random (O)  :", pourcentages(play_game(values, opponent_random) for _ in range(parties)))
    print("greedy (X) vs next   (O)  :", pourcentages(play_game(values, opponent_next) for _ in range(parties)))
    print("etats memorises :", len(values))
