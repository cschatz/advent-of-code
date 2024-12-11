from dataclasses import dataclass
from functools import cache
from typing import List, Set, Tuple

from advent.solver_base import Solver


DIRS = ((0, 1), (1, 0), (0, -1), (-1, 0))


def vadd(a, b):
    return tuple(ai + bi for ai, bi in zip(a, b))


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
    def trails_from(self, trail, locs_in_trail, end_loc):
        height = self.get(*end_loc)
        if height == 9:
            return [trail.with_addition(end_loc)]

        neighbors = filter(
            lambda adj: self.in_bounds(*adj) and self.get(*adj) == height + 1,
            map(
                lambda dir: vadd(loc, dir),
                DIRS
            )
        )
        trails = []
        for neighbor in neighbors:
            trails_in_dir = self.trails_from(neighbor)
            for trail in trails_in_dir:
                if len(trail) == 9 - height:
                    trails.append((loc, *trail))
        return trails

    def solve(self):
        tot = 0
        for r in range(self.rows):
            for c in range(self.cols):
                start_loc = (r, c)
                if self.get(r, c) == 0:
                    num_trails = len(self.trails_from([start_loc], set([start_loc], start_loc)
                    print((r, c), num_trails)
                    tot += num_trails
                    
        return tot

class Part2(Part1):
    ...