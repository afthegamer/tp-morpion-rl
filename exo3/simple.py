import random
from collections import defaultdict

from tictactoe import TicTacToe

PAS = 0.1
EXPLORATION = 0.05


def valeur_initiale():
    # Un etat jamais rencontre vaut 0.5 : "je ne sais pas encore si c'est bon".
    return 0.5


def choisir(values, game, exploration=EXPLORATION):
    # De temps en temps on joue n'importe quoi, sinon on prend le coup dont la
    # grille resultante a la meilleure note (en tirant au sort entre ex aequo).
    if random.random() < exploration:
        return random.choice(game.allowed_moves)
    notes = {case: values[game.state_after(case)] for case in game.allowed_moves}
    meilleure = max(notes.values())
    return random.choice([case for case, note in notes.items() if note == meilleure])


def jouer(values, opponent, exploration=EXPLORATION):
    # ETAPE 1 : on joue une partie et on note juste par quelles grilles X est passe.
    # Ici on n'apprend rien du tout.
    game = TicTacToe()
    etats = []
    while True:
        game.play(choisir(values, game, exploration))
        etats.append(hash(game))
        if game.has_winner():
            return etats, 1.0
        if game.is_draw():
            return etats, 0.0
        game.play(opponent(game))
        if game.has_winner() or game.is_draw():
            return etats, 0.0


def apprendre(values, etats, resultat):
    # ETAPE 2 : on remonte la partie a l'envers avec une seule regle, toujours la meme :
    # chaque grille se rapproche d'un pas de ce qui est arrive JUSTE APRES elle.
    # Pour la derniere, ce qui arrive apres, c'est le resultat reel (1 gagne, 0 sinon).
    cible = resultat
    for etat in reversed(etats):
        values[etat] += PAS * (cible - values[etat])
        cible = values[etat]


def entrainer(values, opponent, parties):
    for _ in range(parties):
        etats, resultat = jouer(values, opponent)
        apprendre(values, etats, resultat)


def taux_de_victoire(values, opponent, parties=10000):
    # On joue sans explorer et sans apprendre : juste pour mesurer le niveau.
    victoires = sum(resultat for _, resultat in
                    (jouer(values, opponent, exploration=0) for _ in range(parties)))
    return f"{100 * victoires / parties:.1f}%"


if __name__ == "__main__":
    from learning import opponent_next, opponent_random

    values = defaultdict(valeur_initiale)
    print("victoires de X vs random, avant :", taux_de_victoire(values, opponent_random))
    entrainer(values, opponent_random, 50000)
    print("victoires de X vs random, apres :", taux_de_victoire(values, opponent_random))

    values = defaultdict(valeur_initiale)
    print("victoires de X vs next,   avant :", taux_de_victoire(values, opponent_next))
    entrainer(values, opponent_next, 50000)
    print("victoires de X vs next,   apres :", taux_de_victoire(values, opponent_next))
