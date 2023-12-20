from heapq import heappush, heappop

from .base import Solver


CONSEC_LIMIT = 3


class Day17(Solver):
    def parse(self, lines): 
        self.grid = tuple(
            tuple(int(x) for x in line)
            for line in lines
        )
        self.height = len(self.grid)
        self.width = len(self.grid[0])

    def cost(self, x, y):
        return self.grid[y][x]

    def in_bounds(self, x, y):
        return (
            x >= 0 and x < self.width
            and y >= 0 and y < self.height
        )
    
    def neighbors(self, pos, dir, dirlen):
        dirs = (
            (_left(dir), _right(dir)) 
            + (dir if dirlen < CONSEC_LIMIT else ())
        )
        return tuple(
            newpos := _step(pos, dir)
            for dir in dirs
            if self.inbounds(newpos)
        )
        
        



class Day17Part1(Day17):
    def solve(self):
        goal = (self.num_rows - 1, self.num_cols - 1)
        start = (0, 0)
        dist = {start: 0}
        prev = dict()
        vertices = set((r, c) for r in range(self.num_rows) for c in range(self.num_cols))
        # each pqueue element: (tot_cost, pos, dir, len of current 'leg')
        vertices.remove((0, 0))
        q = [(0, start, None, 0)]
        while q:
            current = heappop(q)
            if current == goal:
                return dist[current]
            



class Day99Part2(Day17):
    def solve(self):
        ...


def _left(dx, dy):
    # rotate dir vector 90 degrees left
    return (-dy, dx)

def _right(dx, dy):
    # rotate dir vector 90 degrees right
    return (dy, -dx)

def _step(x, y, dx, dy):
    return (x + dx, y + dy)