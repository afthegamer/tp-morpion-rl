from tictactoe import TicTacToe


def main():
    game = TicTacToe()
    while True:
        print(game)
        entree = input(f"Joueur {game.current_player}, ton coup {game.allowed_moves} : ")
        if not entree.isdigit() or not 0 <= int(entree) <= 8:
            print("Entre un numéro de case entre 0 et 8.")
            continue
        joueur = game.current_player
        try:
            game.play(int(entree))
        except ValueError as error:
            print(error)
            continue
        if game.has_winner():
            print(game)
            print(f"Le joueur {joueur} a gagné !")
            break
        if game.is_draw():
            print(game)
            print("Match nul !")
            break


if __name__ == "__main__":
    main()
