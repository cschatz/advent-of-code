import re

from advent.solver_base import Solver

DIGIT_WORDS = (
    "one", "two", "three", "four", "five", "six", "seven", "eight", "nine")


class Part1(Solver):
    PATTERN = r'\d'

    def _item_to_number(self, d):
        return int(d)

    def solve(self):
        def interpret(line):
            all = re.findall(self.PATTERN, line)
            values = [self._item_to_number(d) for d in (all[0], all[-1])]
            return 10 * values[0] + values[1]
        return sum(interpret(line) for line in self.lines)


class Part2(Part1):
    PATTERN = f"(?=(\\d|{'|'.join(DIGIT_WORDS)}))"

    def _item_to_number(self, d):
        return int(d) if d.isdigit() else DIGIT_WORDS.index(d) + 1
