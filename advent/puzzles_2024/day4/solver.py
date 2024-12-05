import re

from ...solver import Solver


DIRS = tuple(
    (dr, dc)
    for dr in (-1, 0, 1)
    for dc in (-1, 0, 1)
    if dr != 0 or dc != 0
)

# diagonal directions need to be in clockwise order
DIAG_DIRS = tuple(
    (dr, dc)
    for dr in (-1, 1)
    for dc in (dr, -dr)
)


# vector addition
def vadd(vecA, vecB):
    return tuple(map(sum, zip(vecA, vecB)))

class Part1(Solver):

    def parse(self, lines):
        self.grid = lines
    
    @property
    def rows(self):
        return len(self.grid)
    
    @property
    def cols(self):
        return len(self.grid[0])
    
    def get(self, pos):
        return self.grid[pos[0]][pos[1]]
    
    def in_bounds(self, r, c):
        return all((r >= 0, c >= 0, r < self.rows, c < self.cols))
    
    def is_word(self, start_pos, dir, word):
        pos = start_pos
        if self.get(pos) != word[0]:
            return False        
        for letter in word[1:]:
            pos = vadd(pos, dir)
            if not self.in_bounds(*pos):
                return False
            if self.get(pos) != letter:
                return False
        return True

    def solve(self):
        return sum(
            self.is_word((r, c), dir, "XMAS")
            for r in range(self.rows)
            for c in range(self.cols)
            for dir in DIRS
        )
    

class Part2(Part1):
    def diag_letters(self, pos):
        return "".join(self.get(vadd(pos, dir)) for dir in DIAG_DIRS)
    

    def is_x_mas(self, pos):
        center = self.get(pos)
        diag = self.diag_letters(pos)
        return (
            center == "A" 
            and diag.count("S") == 2 and diag.count("M") == 2
            and ("MM" in diag or "SS" in diag)
        )

    def solve(self):
        return sum(
            self.is_x_mas((r, c))
            for r in range(1, self.rows - 1)
            for c in range(1, self.cols - 1)
        )
