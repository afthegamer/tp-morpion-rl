from collections import defaultdict

from learning import (evaluer, greedy_move, opponent_next, opponent_random,
                      play_game, play_game2, pourcentages, valeur_initiale)
from tictactoe import TicTacToe

ENTRAINEMENT = 50000

AIDE = """ 0 | 1 | 2
---+---+---
 3 | 4 | 5
---+---+---
 6 | 7 | 8"""


def entrainer(opponent, parties=ENTRAINEMENT):
    values = defaultdict(valeur_initiale)
    for _ in range(parties):
        play_game(values, opponent)
    return values


def demander(game):
    while True:
        entree = input(f"Ton coup (O) {game.allowed_moves} : ")
        if entree.isdigit() and int(entree) in game.allowed_moves:
            return int(entree)
        print("Case invalide.")


def jouer_contre(values):
    game = TicTacToe()
    print(AIDE)
    while True:
        game.play(greedy_move(values, game))
        print()
        print(game)
        if game.has_winner():
            print("L'IA (X) gagne.")
            return
        if game.is_draw():
            print("Match nul.")
            return
        game.play(demander(game))
        print()
        print(game)
        if game.has_winner():
            print("Tu gagnes.")
            return
        if game.is_draw():
            print("Match nul.")
            return


if __name__ == "__main__":
    vierge = defaultdict(valeur_initiale)
    print("vs random, avant entrainement :", evaluer(vierge, opponent_random))
    print("vs next,   avant entrainement :", evaluer(vierge, opponent_next))

    values_random = entrainer(opponent_random)
    print("vs random, apres entrainement :", evaluer(values_random, opponent_random))

    values_next = entrainer(opponent_next)
    print("vs next,   apres entrainement :", evaluer(values_next, opponent_next))

    values_x = defaultdict(valeur_initiale)
    values_o = defaultdict(valeur_initiale)
    for _ in range(ENTRAINEMENT):
        play_game2(values_x, values_o)
    print("self-play, apres entrainement :", pourcentages(play_game2(values_x, values_o, step=0, exploration=0) for _ in range(10000)))

    print()
    jouer_contre(values_next)
