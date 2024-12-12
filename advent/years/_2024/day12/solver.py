from collections import defaultdict
# Note: needs python 3.10 or newer
from itertools import pairwise

from advent.solver_base import Solver


DIRS = ((0, 1), (1, 0), (0, -1), (-1, 0))


def vadd(a, b):
    return tuple(ai + bi for ai, bi in zip(a, b))

def make_fence(r, c, dr, dc):
    # (direction, coord on axis that fence parallels
    if dr: 
        return ((dr, dc), r, c)
    else:
        return ((dr, dc), c, r)


class Day12(Solver):
    def parse(self, lines):
        self.garden = lines
        self.rows = len(lines)
        self.cols = len(lines[0])

    def get(self, r, c):
        return self.garden[r][c]
    
    def in_bounds(self, r, c):
        return all((r >= 0, c >= 0, r < self.rows, c < self.cols))

    def survey_region(self, start_plot):
        plant_type = self.get(*start_plot)
        in_region = set()
        fences = set()
        stack = [start_plot]
        while len(stack) > 0:
            current = stack.pop()
            if current not in in_region:
                in_region.add(current)
                for dir in DIRS:
                    neighbor = vadd(current, dir)
                    if not self.in_bounds(*neighbor) or self.get(*neighbor) != plant_type:
                        fences.add(make_fence(*current,* dir))
                    else:
                        stack.append(neighbor)
        return len(in_region), fences, in_region
    
    def get_regions(self):
        unsurveyed_plots = set([
            (r, c)
            for r in range(self.rows)
            for c in range(self.cols)
        ])
        regions = []
        while unsurveyed_plots:
            plot = next(iter(unsurveyed_plots))
            area, fences, plots = self.survey_region(plot)
            unsurveyed_plots -= plots
            regions.append((area, fences))
        return regions

class Part1(Day12):
    def solve(self):
        regions = self.get_regions()
        return sum(
            area * len(fences) for area, fences in regions
        )
    

def count_sides(fences):
    groups = defaultdict(set)
    for side, group_num, pos in fences:
        groups[(side, group_num)].add(pos)
    return sum(
        sum(
            b - a > 1
            for a, b in pairwise(sorted(positions))
        ) + 1
        for positions in groups.values()
    )
        

class Part2(Part1):
    def solve(self):
        regions = self.get_regions()
        return sum(
            area * count_sides(fences) for area, fences in regions
        )