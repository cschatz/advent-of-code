import re

from .base import Solver


class Day1Solver(Solver):

    def solve(self, part, *lines):
        items = ["\\d"]
        if part == 2:
            items.extend(ENG_DIGITS.keys())
        pattern = f"(?=({'|'.join(items)}))"

        def interpret(line):
            all = re.findall(pattern, line)
            # overkill for just first and last, but easy to
            # adapt to more than 2 digits
            tot = 0
            for d in (all[0], all[-1]):
                tot *= 10
                n = int(d) if d.isdigit() else ENG_DIGITS[d]
                tot += n
            return tot

        return sum(interpret(line) for line in lines)


ENG_DIGITS = dict(
    one=1,
    two=2,
    three=3,
    four=4,
    five=5,
    six=6,
    seven=7,
    eight=8,
    nine=9,
)
