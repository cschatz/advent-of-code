import re

from .base import Solver

DIGIT_WORDS = ("one", "two", "three", "four", "five",
               "six", "seven", "eight", "nine")


class Day1Solver(Solver):

    def solve(self, part, *lines):
        items = ("\\d",) + (DIGIT_WORDS if part == 2 else ())
        # include overlapping matches
        pattern = f"(?=({'|'.join(items)}))"

        def interpret(line):
            all = re.findall(pattern, line)
            tot = 0
            for d in (all[0], all[-1]):
                tot *= 10
                n = int(d) if d.isdigit() else DIGIT_WORDS.index(d) + 1
                tot += n
            return tot

        return sum(interpret(line) for line in lines)
