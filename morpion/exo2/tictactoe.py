EMPTY = " "
PLAYER_X = "X"
PLAYER_O = "O"

WINNING_LINES = [
    (0, 1, 2), (3, 4, 5), (6, 7, 8),
    (0, 3, 6), (1, 4, 7), (2, 5, 8),
    (0, 4, 8), (2, 4, 6),
]


class TicTacToe:
    def __init__(self):
        self.grid = [EMPTY] * 9
        self.current_player = PLAYER_X

    def play(self, case):
        if self.grid[case] != EMPTY:
            raise ValueError(f"La case {case} est déjà occupée.")
        self.grid[case] = self.current_player
        self._switch_player()

    def __str__(self):
        rows = [" " + " | ".join(self.grid[i:i + 3]) + " " for i in range(0, 9, 3)]
        return "\n---+---+---\n".join(rows)

    def __hash__(self):
        return hash("".join(self.grid))

    def has_winner(self):
        return any(
            self.grid[a] != EMPTY and self.grid[a] == self.grid[b] == self.grid[c]
            for a, b, c in WINNING_LINES
        )

    def is_draw(self):
        return EMPTY not in self.grid and not self.has_winner()

    def reset(self):
        self.grid = [EMPTY] * 9
        self.current_player = PLAYER_X

    def undo(self, case):
        self.grid[case] = EMPTY
        self._switch_player()

    @property
    def allowed_moves(self):
        return [case for case, cell in enumerate(self.grid) if cell == EMPTY]

    def _switch_player(self):
        self.current_player = PLAYER_O if self.current_player == PLAYER_X else PLAYER_X
