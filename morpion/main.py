from tictactoe import TicTacToe

if __name__ == "__main__":
    game = TicTacToe()
    print(game)
    print("Coups possibles :", game.allowed_moves)

    game.play(0)  # X
    game.play(4)  # O
    game.play(1)  # X
    game.play(5)  # O
    game.play(2)  # X gagne la ligne du haut

    print()
    print(game)
    print("Gagnant ?", game.has_winner())
    print("Match nul ?", game.is_draw())

    game.undo(2)
    print()
    print("Après undo(2) :")
    print(game)
    print("Coups possibles :", game.allowed_moves)

    game.reset()
    print()
    print("Après reset :")
    print(game)
