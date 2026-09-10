import random
from collections import defaultdict, Counter

from tictactoe import TicTacToe, PLAYER_X, PLAYER_O


def opponent_random(tictactoe: TicTacToe) -> int:
    """Joueur aléatoire pour l'adversaire"""
    return random.choice(tictactoe.allowed_moves)


def opponent_next(tictactoe: TicTacToe) -> int:
    """Joueur joue un coup gagnant si possible, sinon aléatoire"""
    for move in tictactoe.allowed_moves:
        tictactoe.play(move)
        if tictactoe.has_winner():
            tictactoe.undo(move)
            return move
        tictactoe.undo(move)
    return opponent_random(tictactoe)


def greedy_move(values, tictactoe: TicTacToe) -> int:
    """Joueur qui choisit le coup avec la meilleure valeur"""
    scores = {}
    for move in tictactoe.allowed_moves:
        tictactoe.play(move)
        scores[move] = values[hash(tictactoe)]
        tictactoe.undo(move)
    best_score = max(scores.values())
    best_moves = [move for move, score in scores.items() if score == best_score]
    return random.choice(best_moves)


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


values = defaultdict(lambda: 0.5)

if __name__ == "__main__":
    parties = 10000
    print("random (X) vs random (O)  :", pourcentages(play_game(values, opponent_random) for _ in range(parties)))
    print("next   (X) vs random (O)  :", pourcentages(play_game(values, opponent_next) for _ in range(parties)))
    print("random (X) vs next   (O)  :", pourcentages(play_game(values, opponent_random) for _ in range(parties)))
    print("greedy (X) vs random (O)  :", pourcentages(play_game(values, opponent_random) for _  in range(parties)))
    print("greedy (X) vs next   (O)  :", pourcentages(play_game(values, opponent_next) for _ in range(parties)))
    print("etats memorises :", len(values))
