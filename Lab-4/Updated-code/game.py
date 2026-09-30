import time
from puzzle import Puzzle


class SlidingPuzzle:
    def __init__(self, size=4):
        self.size = size
        self.puzzle = Puzzle(self.size)
        self.moves = 0
        self.started = time.monotonic()
        self.finished = False

    def display(self):
        print()
        for row in self.puzzle.board:
            print(" ".join(f"{x or ' ':>2}" for x in row))
        print("Moves:", self.moves, " Time:", int(time.monotonic() - self.started), "s")

    def select_size(self):
        while True:
            choice = input("Choose puzzle size (3/4/5): ").strip()
            if choice in ("3", "4", "5"):
                self.size = int(choice)
                self.puzzle = Puzzle(self.size)
                self.moves = 0
                self.started = time.monotonic()
                self.finished = False
                return
            print("Choose 3, 4, or 5.")

    def run(self):
        print("Sliding Puzzle — W/A/S/D moves the tile into the blank. Q quits.")
        self.select_size()
        while not self.finished:
            self.display()
            if self.puzzle.solved():
                self.finished = True
                print("Solved!")
                return
            key = input("> ").strip().lower()
            if key == "q":
                return
            if key not in "wasd":
                print("Use W/A/S/D.")
                continue
            if self.puzzle.move(key):
                self.moves += 1
                if self.puzzle.solved():
                    self.finished = True
                    self.display()
                    print("Solved!")
                    return
            else:
                print("That move is not possible.")
