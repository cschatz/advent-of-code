from collections import defaultdict
from math import gcd

from advent.solver_base import Solver


class Part1(Solver):
    def parse(self, lines):
        self.rows = len(lines)
        self.cols = len(lines[0])
        self.antennas = defaultdict(list)
        for r, line in enumerate(lines):
            for c, cell in enumerate(line):
                if cell != ".":
                    self.antennas[cell].append((r, c))

    def in_bounds(self, r, c):
        return all((r >= 0, c >= 0, r < self.rows, c < self.cols))

    def solve(self):
        locations = set()
        for antenna_set in self.antennas.values():
            for antenna_pair in pairs(antenna_set):
                for loc in antinodes(*antenna_pair):
                    if self.in_bounds(*loc):
                        locations.add(loc)
        return len(locations)


class Part2(Part1):
    def solve(self):
        locations = set()
        for antenna_set in self.antennas.values():
            for antenna_pair in pairs(antenna_set):
                a, b = antenna_pair
                step_fwd = slope(a, b)
                step_rev = vneg(step_fwd)
                for start_loc, step in zip((b, a), (step_fwd, step_rev)):
                    for loc in locs_from(start_loc, step):
                        if not self.in_bounds(*loc):
                            break
                        locations.add(loc)
        return len(locations)


def vadd(a, b):
    return tuple(ai + bi for ai, bi in zip(a, b))


def vsub(a, b):
    return tuple(ai - bi for ai, bi in zip(a, b))


def vneg(a):
    return tuple(-ai for ai in a)


def pairs(items):
    return tuple(
        (items[i], x)
        for i in range(len(items))
        for x in items[i + 1:]
    )


def antinodes(a, b):
    diff = vsub(b, a)
    return (
        vadd(b, diff),
        vsub(a, diff)
    )


def slope(a, b):
    diff = vsub(b, a)
    scale = gcd(*diff)
    return tuple(x // scale for x in diff)


def locs_from(start_loc, step):
    loc = start_loc
    while True:
        yield loc
        loc = vadd(loc, step)
