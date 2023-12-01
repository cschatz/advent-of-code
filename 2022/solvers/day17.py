from util import input_all

PIECES = """####

.#.
###
.#.

..#
..#
###

#
#
#
#

##
##"""

WIDTH = 7

def translate(lst, delta):
    return [list(map(sum, zip(delta, x))) for x in lst]

def cycle(items):
    while True:
        for item in items:
            yield item

def parse(diagram):
    rocks = []
    rows = diagram.split("\n")
    h = len(rows)
    for r, row in enumerate(rows):
        for c, col in enumerate(row):
            if col == "#":
                rocks.append([h - 1 - r, c])
    return rocks, h

class Tetris:
    def __init__(self, jets):
        self.pieces = cycle([parse(p) for p in PIECES.split("\n\n")])
        self.jets = cycle(jets)
        self.grid = []

    def start_fall(self):
        self.piece, h = next(self.pieces)
        self.piece = translate(self.piece, (len(self.grid) + 3, 2))
        self.grid.extend(
            [[False for _ in range(WIDTH)] for _ in range(3 + h)])

    def check(self, pos):
        if pos in self.piece:
            return True
        r, c = pos
        if r < 0 or c < 0 or c >= WIDTH:
            return False
        if self.grid[r][c] is True:
            return False
        return True

    def push(self, delta):
        new_pos = translate(self.piece, delta)
        ok = all(self.check(p) for p in new_pos)
        if ok:
            self.piece = new_pos
        return ok

    def tick(self):
        jet = next(self.jets)
        jet_push = (0, 1) if jet is True else (0, -1)
        self.push(jet_push)
        return self.push((-1, 0))

    def one_round(self):
        self.start_fall()
        while self.tick() is True:
            pass
        for r, c in self.piece:
            self.grid[r][c] = True
        while not any(self.grid[-1]):
            self.grid.pop()

    def display(self):
        for row in self.grid[::-1]:
            contents = "".join("#" if x else "." for x in row)
            print("|" + contents + "|")
        print("+" + ("-" * WIDTH) + "+")

def day17_parse(file):
    symbols = input_all(file)
    jets = [True if x == ">" else False for x in symbols]
    return (Tetris(jets),)

def day17_1(t):
    for _ in range(2022):
        t.one_round()
    return len(t.grid)

def day17_2(t):
    pass

