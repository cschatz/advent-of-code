import re
from functools import reduce
from operator import mul

from .base import Solver

COLORS = ("red", "green", "blue")


class Day2(Solver):
    def parse(self, lines):
        def process(line):
            return tuple(
                tuple(
                    int(m.group(1))
                    if (m := re.search(f"(\\d+) {color}", draw))
                    else 0
                    for color in COLORS
                )
                for draw in line.split("; ")
            )
        self.games = [process(line) for line in lines]


class Day2Part1(Day2):
    def solve(self):
        MAXES = (12, 13, 14)
        return sum(
            index for index, game in enumerate(self.games, 1)
            if all(
                all(counts[i] <= MAXES[i] for i in range(3))
                for counts in game
            )
        )


class Day2Part2(Day2):
    def solve(self):
        return sum(
            reduce(mul, (max(counts) for counts in zip(*game)), 1)
            for game in self.games
        )
    

