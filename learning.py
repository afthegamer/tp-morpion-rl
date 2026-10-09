import random
from collections import defaultdict, Counter

from tictactoe import TicTacToe, PLAYER_X, PLAYER_O


def valeur_initiale() -> float:
    """Valeur d'un état jamais rencontré (fonction nommée : une lambda n'est pas picklable)"""
    return 0.5


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


def play_opponents(first, second):
    """Partie complète entre deux fonctions d'adversaire, sans value function"""
    game = TicTacToe()
    players = (first, second)
    turn = 0
    while True:
        player = game.curent_player
        game.play(players[turn](game))
        if game.has_winner():
            return player
        if game.is_draw():
            return None
        turn = 1 - turn


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


def update(values, state, target, step) -> None:
    """Temporal-difference : V(s) <- V(s) + step * (target - V(s))"""
    if state is not None:
        values[state] += step * (target - values[state])


def play_game(values, opponent, step=0.1):
    """Partie greedy (X) contre opponent (O), avec mise à jour de la value function"""
    game = TicTacToe()
    previous = None  # état après notre coup précédent, corrigé dès qu'on voit la suite
    while True:
        game.play(greedy_move(values, game))
        state = hash(game)

        if game.has_winner():
            values[state] = 1.0  # partie terminée : valeur exacte, plus une estimation
            update(values, previous, 1.0, step)
            return PLAYER_X
        if game.is_draw():
            values[state] = 0.0  # l'énoncé impose 0 ou 1 : le nul compte comme une défaite
            update(values, previous, 0.0, step)
            return None

        update(values, previous, values[state], step)  # TD après chaque coup
        previous = state

        game.play(opponent(game))
        if game.has_winner():
            update(values, previous, 0.0, step)
            return PLAYER_O
        if game.is_draw():
            update(values, previous, 0.0, step)
            return None


def pourcentages(resultats):
    compteur = Counter(resultats)
    total = sum(compteur.values())
    return {(cle or "nul"): f"{100 * compteur[cle] / total:.1f}%" for cle in (PLAYER_X, PLAYER_O, None)}


if __name__ == "__main__":
    parties = 10000
    print("random (X) vs random (O) :", pourcentages(play_opponents(opponent_random, opponent_random) for _ in range(parties)))
    print("next   (X) vs random (O) :", pourcentages(play_opponents(opponent_next, opponent_random) for _ in range(parties)))
    print("random (X) vs next   (O) :", pourcentages(play_opponents(opponent_random, opponent_next) for _ in range(parties)))

    for opponent in (opponent_random, opponent_next):
        values = defaultdict(valeur_initiale)
        for bloc in range(5):
            resultats = pourcentages(play_game(values, opponent) for _ in range(parties))
            print(f"greedy (X) vs {opponent.__name__[9:]:<6} (O), parties {bloc * parties:>5}-{(bloc + 1) * parties:<5} :", resultats)
        print("etats memorises :", len(values))
