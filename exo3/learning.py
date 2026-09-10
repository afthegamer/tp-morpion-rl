import random
from collections import Counter, defaultdict

from tictactoe import PLAYER_O, PLAYER_X, TicTacToe


def valeur_initiale():
    return 0.5


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


def greedy_move(values, game):
    scores = {case: values[game.state_after(case)] for case in game.allowed_moves}
    meilleur = max(scores.values())
    return random.choice([case for case, valeur in scores.items() if valeur == meilleur])


def choose_move(values, game, exploration):
    if random.random() < exploration:
        return random.choice(game.allowed_moves)
    return greedy_move(values, game)


def update(values, etat, cible, step):
    # Formule de la temporal-difference : on rapproche la valeur de `etat` de `cible`
    # d'une fraction `step` de l'ecart. step = 0 -> on n'apprend rien (mode evaluation).
    if etat is not None:
        values[etat] += step * (cible - values[etat])


def play_game(values, opponent, step=0.1, exploration=0.05):
    # Une partie complete : nous jouons X, `opponent` joue O.
    # `values` note les grilles OBTENUES APRES NOTRE COUP : c'est exactement ce que
    # greedy_move compare pour choisir. La valeur = probabilite estimee que X gagne.
    game = TicTacToe()
    precedent = None  # notre coup precedent, dont la valeur attend d'etre corrigee
    while True:
        game.play(choose_move(values, game, exploration))
        etat = hash(game)

        if game.has_winner():
            # Partie finie : ce n'est plus une estimation, cet etat vaut 1 par definition.
            if step:
                values[etat] = 1.0
            # Et on apprend a notre coup precedent qu'il menait a une victoire.
            update(values, precedent, 1.0, step)
            return PLAYER_X
        if game.is_draw():
            # L'enonce impose 0 ou 1 : le nul compte donc comme une defaite.
            if step:
                values[etat] = 0.0
            update(values, precedent, 0.0, step)
            return None

        # Le coeur de la methode : on corrige le coup precedent vers la valeur de l'etat
        # atteint depuis, sans attendre la fin de la partie. L'info remonte d'un cran
        # a chaque coup, et de proche en proche jusqu'au debut au fil des parties.
        update(values, precedent, values[etat], step)
        precedent = etat

        game.play(opponent(game))
        # L'adversaire vient de jouer : si ca tourne mal, c'est notre dernier coup
        # (precedent) qui est sanctionne. On ne l'ecrase PAS a 0 : la position n'est pas
        # perdante en soi, elle l'est parce que CET adversaire a su en profiter.
        if game.has_winner():
            update(values, precedent, 0.0, step)
            return PLAYER_O
        if game.is_draw():
            update(values, precedent, 0.0, step)
            return None


def play_game2(values_x, values_o, step=0.1, exploration=0.05):
    # Meme chose, mais les deux joueurs apprennent, chacun avec SA table.
    # Aucun risque de melange : X ne note que les grilles ou il vient de jouer
    # (autant de X que de O + 1), O que les siennes (autant de X que de O).
    game = TicTacToe()
    valeurs = (values_x, values_o)
    precedents = [None, None]  # un coup en attente de correction par joueur
    tour = 0
    while True:
        joueur = game.current_player
        values = valeurs[tour]
        game.play(choose_move(values, game, exploration))
        etat = hash(game)

        if game.has_winner():
            if step:
                values[etat] = 1.0
            # Jeu a somme nulle : celui qui vient de jouer gagne (1), l'autre perd (0).
            update(values, precedents[tour], 1.0, step)
            update(valeurs[1 - tour], precedents[1 - tour], 0.0, step)
            return joueur
        if game.is_draw():
            if step:
                values[etat] = 0.0
            update(values, precedents[tour], 0.0, step)
            update(valeurs[1 - tour], precedents[1 - tour], 0.0, step)
            return None

        update(values, precedents[tour], values[etat], step)
        precedents[tour] = etat
        tour = 1 - tour


def pourcentages(resultats):
    compteur = Counter(resultats)
    total = sum(compteur.values())
    return {(cle or "nul"): f"{100 * compteur[cle] / total:.1f}%" for cle in (PLAYER_X, PLAYER_O, None)}


def evaluer(values, opponent, parties=10000):
    return pourcentages(play_game(values, opponent, step=0, exploration=0) for _ in range(parties))
