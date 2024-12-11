from functools import cache

from advent.solver_base import Solver


DIRS = ((0, 1), (1, 0), (0, -1), (-1, 0))


def vadd(a, b):
    return tuple(ai + bi for ai, bi in zip(a, b))

def peaks(trails):
    return len(set([trail[-1] for trail in trails]))

class Part1(Solver):
    def parse(self, lines):
        self.topo = [
            [int(x) for x in line]
            for line in lines
        ]
        self.rows = len(lines)
        self.cols = len(lines[0])

    def get(self, r, c):
        return self.topo[r][c]
    
    def in_bounds(self, r, c):
        return all((r >= 0, c >= 0, r < self.rows, c < self.cols))

    @cache
    def trails_from(self, trail, loc, loc_set):
        height = self.get(*loc)
        if height == 9:
            return [trail]
        neighbors = (
            adj for dir in DIRS
            if (
                (adj := vadd(loc, dir)) not in loc_set
                and self.in_bounds(*adj)
                and self.get(*adj) == height + 1
            )    
        )
        return [
            trail_in_dir
            for neighbor in neighbors
            for trail_in_dir in self.trails_from(trail + (neighbor,), neighbor, loc_set | frozenset((neighbor,)))
        ]

    def solve(self):
        return sum(
            peaks(self.trails_from((start,), start, frozenset((start,))))
            for r in range(self.rows)
            for c in range(self.cols)
            if self.get(*(start := (r, c))) == 0
        )
                    
class Part2(Part1):
    def solve(self):
        return sum(
            len(self.trails_from((start,), start, frozenset((start,))))
            for r in range(self.rows)
            for c in range(self.cols)
            if self.get(*(start := (r, c))) == 0
        )