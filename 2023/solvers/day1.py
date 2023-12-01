import re

from .base import Solver

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

PLAIN_PAT = "(?=(\\d))"
EXPANDED_PAT = f"(?=(\\d|{'|'.join(ENG_DIGITS.keys())}))"


def make_pattern(part):
    items = ["\\d"]
    if part == 2:
        items.extend(ENG_DIGITS.keys())
    return f"(?=({'|'.join(items)}))"


def to_int(s):
    if s.isdigit():
        return int(s)
    else:
        return ENG_DIGITS[s]


class Day1Solver(Solver):

    def solve(self, part, *lines):
        pat = make_pattern(part)

        def interpret(line):
            all = re.findall(pat, line)
            digits = tuple(map(to_int, (all[0], all[-1])))
            return int(digits[0]) * 10 + int(digits[1])
        return sum(interpret(line) for line in lines)

