import random
from collections import Counter

from tictactoe import PLAYER_O, PLAYER_X, TicTacToe


def opponent_random(game):
    return random.choice(game.allowed_moves)


def opponent_next(game):
    for case in game.allowed_moves:
        game.play(case)
        gagnant = game.has_winner()
        game.undo(case)
        if gagnant:
            return case
    return random.choice(game.allowed_moves)


def play_opponents(first, second):
    game = TicTacToe()
    joueurs = (first, second)
    tour = 0
    while True:
        joueur = game.current_player
        game.play(joueurs[tour](game))
        if game.has_winner():
            return joueur
        if game.is_draw():
            return None
        tour = 1 - tour


def greedy_move(values, game):
    scores = {}
    for case in game.allowed_moves:
        game.play(case)
        scores[case] = values[hash(game)]
        game.undo(case)
    meilleur = max(scores.values())
    return random.choice([case for case, valeur in scores.items() if valeur == meilleur])


def play_game(values, opponent):
    game = TicTacToe()
    while True:
        game.play(greedy_move(values, game))
        if game.has_winner():
            return PLAYER_X
        if game.is_draw():
            return None
        game.play(opponent(game))
        if game.has_winner():
            return PLAYER_O
        if game.is_draw():
            return None


def pourcentages(resultats):
    compteur = Counter(resultats)
    total = sum(compteur.values())
    return {(cle or "nul"): f"{100 * compteur[cle] / total:.1f}%" for cle in (PLAYER_X, PLAYER_O, None)}
