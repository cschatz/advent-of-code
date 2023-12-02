import re
from functools import reduce
from operator import mul

from .base import Solver

COLORS = ("red", "green", "blue")


class Day2Solver(Solver):

    def parse(self, file):
        def parse_line(line):
            line = re.sub(r'Game \d+: ', "", line)
            return tuple(parse_handful(h) for h in line.split("; "))

        def parse_handful(handful):
            counts = [0, 0, 0]
            for piece in handful.split(", "):
                count, color = piece.split(" ")
                counts[COLORS.index(color)] = int(count)
            return counts

        lines = Solver.input_lines(file)
        return [parse_line(line) for line in lines]

    def solve_part1(self, *games):
        MAXES = (12, 13, 14)
        sum = 0
        for index, game in enumerate(games, 1):
            if all(all(counts[i] <= MAXES[i] for i in range(3)) for counts in game):
                sum += index
        return sum

    def solve_part2(self, *games):
        return sum(
            reduce(mul, (max(counts) for counts in zip(*game)), 1)
            for game in games
        )
