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

    def num_matches(self, card):
        return sum(n in card[0] for n in card[1])
    

class Day4Part1(Day4):
    def solve(self):
       return sum(
           1 << (m - 1)
           for card in self.cards
           if (m := self.num_matches(card)) > 0
       )           

class Day4Part2(Day4):
    def solve(self):
        counts = [1 for _ in range(len(self.cards))]
        for i, card in enumerate(self.cards):
            for j in range(i + 1, i + 1 + self.num_matches(card)):
                counts[j] += counts[i]
        return sum(counts)
