from heapq import heappush, heappop

from .base import Solver



class Day17(Solver):
    def parse(self, lines): 
        self.grid = tuple(
            tuple(int(x) for x in line)
            for line in lines
        )
        self.num_rows = len(self.grid)
        self.num_cols = len(self.grid[0])

    def cost(self, r, c):
        return self.grid[r][c]

    def in_bounds(self, r, c):
        return (
            r >= 0 and r < self.num_rows
            and c >= 0 and c < self.num_cols
        )


class Day17Part1(Day17):
    def solve(self):
        goal = (self.num_rows - 1, self.num_cols - 1)
        start = (0, 0) 
        dist = {start: 0}
        prev = dict()
        vertices = set((r, c) for r in range(self.num_rows) for c in range(self.num_cols))
        

class Day99Part2(Day17):
    def solve(self):
        ...