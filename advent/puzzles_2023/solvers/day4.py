import re

from .base import Solver


class Day4(Solver):
    def parse(self, lines):
        def process(line):
            pieces = re.sub("^.+: ", "", line).split(" | ")
            return tuple(
                set(int(x) for x in re.split(" +", p) if x.isdigit())
                for p in pieces
            )
        self.cards = [process(line) for line in lines]


class Day4Part1(Day4):
    def solve(self):
       return sum(
           1 << (m - 1)
           for card in self.cards
           if (m := _matches(*card)) > 0
       )           


class Day4Part2(Day4):
    def solve(self):
        counts = [1 for _ in range(len(self.cards))]
        for i, card in enumerate(self.cards):
            for j in range(i + 1, i + 1 + _matches(*card)):
                counts[j] += counts[i]
        return sum(counts)


def _matches(a, b):
    return len(a & b)  # set intersection