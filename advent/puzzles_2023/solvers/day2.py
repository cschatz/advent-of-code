import re
from functools import reduce
from operator import mul

from .base import Solver

COLORS = ("red", "green", "blue")


class Day2Solver(Solver):

    def parse(self, file):
        def parse_line(line):
            return tuple(
                tuple(
                    int(m.group(1))
                    if (m := re.search(f"(\\d+) {color}", draw))
                    else 0
                    for color in COLORS
                )
                for draw in line.split("; ")
            )
        return [parse_line(line) for line in file.readlines()]

    def solve_part1(self, *games):
        MAXES = (12, 13, 14)
        return sum(
            index for index, game in enumerate(games, 1)
            if all(
                all(counts[i] <= MAXES[i] for i in range(3))
                for counts in game
            )
        )

    def solve_part2(self, *games):
        return sum(
            reduce(mul, (max(counts) for counts in zip(*game)), 1)
            for game in games
        )
