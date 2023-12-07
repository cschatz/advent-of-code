import re
from math import floor, sqrt

from .base import Solver


class Day6(Solver):
    def solve(self):
        product = 1
        for time, distance in self.races:
            product *= _solve_race(time, distance)
        return product


class Day6Part1(Day6):
    def parse(self, lines):
        self.races = zip(
            *tuple(
                tuple(int(x) for x in re.findall(r'(\d+)', line))
                for line in lines
            )
        )


class Day6Part2(Day6):
    def parse(self, lines):
        self.races = [
            tuple(
                int(''.join(re.findall(r'(\d+)', line)))
                for line in lines
            )
        ]


def _solve_race(t, d):
    quad_root = (t - sqrt(t ** 2 - 4 * d)) / 2
    return t + 1 - 2 * (floor(quad_root) + 1)
