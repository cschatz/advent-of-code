import re

from .base import Solver

DIGIT_WORDS = (
    "one", "two", "three", "four", "five", "six", "seven", "eight", "nine")


class Day1Part1(Solver):
    PATTERN = r'\d'

    def _item_to_number(self, d):
        return int(d)

    def solve(self):
        def interpret(line):
            all = re.findall(self.PATTERN, line)
            values = [self._item_to_number(d) for d in (all[0], all[-1])]
            return 10 * values[0] + values[1]
        return sum(interpret(line) for line in self.lines)


class Day1Part2(Day1Part1):
    PATTERN = f"(?=(\\d|{'|'.join(DIGIT_WORDS)}))"

    def _item_to_number(self, d):
        return int(d) if d.isdigit() else self.DIGIT_WORDS.index(d) + 1
