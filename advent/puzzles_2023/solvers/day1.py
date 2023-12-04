import re

from .base import Solver


class Day1Part1(Solver):
    @property
    def pattern(self):
        return r'\d'

    def solve(self):
        def interpret(line):
            all = re.findall(self.pattern, line)
            tot = 0
            for d in (all[0], all[-1]):
                tot *= 10
                tot += self._item_to_number(d)
            return tot

        return sum(interpret(line) for line in self.lines)

    def _item_to_number(self, d):
        return int(d)


class Day1Part2(Day1Part1):
    DIGIT_WORDS = (
        "one", "two", "three", "four", "five", "six", "seven", "eight", "nine")

    @property
    def pattern(self):
        return f"(?=(\\d|{'|'.join(self.DIGIT_WORDS)}))"

    def _item_to_number(self, d):
        return int(d) if d.isdigit() else self.DIGIT_WORDS.index(d) + 1
