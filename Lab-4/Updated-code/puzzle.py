import random


class Puzzle:
    def __init__(self, size=4):
        self.size = size
        self.board = self.make_board()

    def make_board(self):
        board = [list(range(r * self.size + 1, (r + 1) * self.size + 1))
                 for r in range(self.size)]
        board[-1][-1] = 0
        self.board = board

        # Scramble only through legal blank moves, so every generated
        # board remains reachable from the solved arrangement.
        directions = ["w", "s", "a", "d"]
        for _ in range(self.size * self.size * 20):
            r, c = self.blank_pos()
            legal = []
            for direction in directions:
                dr, dc = {
                    "w": (-1, 0),
                    "s": (1, 0),
                    "a": (0, -1),
                    "d": (0, 1),
                }[direction]
                nr, nc = r + dr, c + dc
                if 0 <= nr < self.size and 0 <= nc < self.size:
                    legal.append(direction)
            self.move(random.choice(legal))

        return self.board

    def blank_pos(self):
        for r in range(self.size):
            for c in range(self.size):
                if self.board[r][c] == 0:
                    return r, c

    def move(self, direction):
        r, c = self.blank_pos()
        dr, dc = {"w": (-1, 0), "s": (1, 0), "a": (0, -1), "d": (0, 1)}[direction]
        nr, nc = r + dr, c + dc
        if not (0 <= nr < self.size and 0 <= nc < self.size):
            return False
        self.board[r][c], self.board[nr][nc] = self.board[nr][nc], self.board[r][c]
        return True

    def solved(self):
        return sum(self.board, []) == list(range(1, self.size * self.size)) + [0]
