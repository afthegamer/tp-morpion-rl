EMPTY = " "
PLAYER_X = "X"
PLAYER_O = "O"

WINING_LINES = [
    (0, 1, 2), (3, 4, 5), (6, 7, 8),  # lignes
    (0, 3, 6), (1, 4, 7), (2, 5, 8),  # colonnes
    (0, 4, 8), (2, 4, 6),             # diagonales
]

class TicTacToe:
    def __init__(self):
        self.grid = [EMPTY] * 9
        self.curent_player = PLAYER_X
        self.next_player = PLAYER_O

    def play(self, case:int) -> None:
        if not (0 <= case <= 8) or self.grid[case] != EMPTY:
            raise ValueError(f"Case invalide : {case} (doit être entre 0 et 8)")
        if self.grid[case] != EMPTY:
            raise ValueError(f"Case déjà occupée : {case}")

        self.grid[case] = self.curent_player
        self.curent_player = PLAYER_O if self.curent_player == PLAYER_X else PLAYER_X

    def undo(self, case:int) -> None:
        if not (0 <= case <= 8) or self.grid[case] == EMPTY:
            raise ValueError(f"Case invalide : {case} (doit être entre 0 et 8)")
        if self.grid[case] == EMPTY:
            raise ValueError(f"Case déjà vide : {case}")

        self.curent_player = self.grid[case]
        self.grid[case] = EMPTY

    def has_winner(self) -> bool:
        for line in WINING_LINES:
            if self.grid[line[0]] != EMPTY and self.grid[line[0]] == self.grid[line[1]] == self.grid[line[2]]:
                return True
        return False

    def is_draw (self) -> bool:
        return EMPTY not in self.grid and not self.has_winner()

    def is_over(self) -> bool:
        return self.has_winner() or self.is_draw()

    def reset(self) -> None:
        self.grid = [EMPTY] * 9
        self.curent_player = PLAYER_X

    @property
    def allowed_moves(self) -> list[int]:
        return [i for i, cell in enumerate(self.grid) if cell == EMPTY]

    def __str__(self) -> str:
        rows = [" " + " | ".join(self.grid[i:i + 3]) + " " for i in range(0, 9, 3)]
        return "\n---+---+---\n".join(rows)

    def __hash__(self) -> int:
        return hash("".join(self.grid))