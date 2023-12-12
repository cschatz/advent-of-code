from .base import Solver


def _rev(dir):
    return tuple(-a for a in dir)


def _pipe(dirA, dirB):
    return {
        dirA: dirB,
        _rev(dirB): _rev(dirA),
    }


PIPES = {
    "|": _pipe((1, 0), (1, 0)),
    "-": _pipe((0, 1), (0, 1)),
    "L": _pipe((1, 0), (0, 1)),
    "J": _pipe((1, 0), (0, -1)),
    "7": _pipe((-1, 0), (0, -1)),
    "F": _pipe((-1, 0), (0, 1)),
    ".": None,
}


class Day10(Solver):
    def parse(self, lines):
        ...


class Day10Part1(Day10):
    def solve(self):
        ...


class Day10Part2(Day10):
    def solve(self):
        ...

