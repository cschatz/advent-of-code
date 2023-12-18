from collections import defaultdict

from .base import Solver


DIRS = {
    "R": (0, 1),
    "L": (0, -1),
    "U": (-1, 0),
    "D": (1, 0),
}

def go(loc, dir, len):
    return tuple(a + b * len for a, b in zip(loc, dir))


class Day18(Solver):
    def solve(self):
        current = (0, 0)
        v = [current]
        perimeter = 0
        for dir, dist in self.steps:
            current = go(current, dir, dist)
            perimeter += dist
            v.append(current)
        area = sum(
            (v[i + 1][1] + v[i][1]) * (v[i + 1][0] - v[i][0])
            for i in range(0, len(v) - 1)
        ) // 2
        return area + perimeter // 2 + 1


class Day18Part1(Day18):
    def parse(self, lines):
        def _parse(line):
            dir, dist, _ = line.split(" ")
            dir = DIRS[dir]
            dist = int(dist)
            return (dir, dist)
        self.steps = [_parse(line) for line in lines]

            
class Day18Part2(Day18):
    def parse(self, lines):
        def _parse(line):
            _, _, hex = line.split(" ")
            hex = hex[2:-1]
            dir = "RDLU"[int(hex[-1])]
            dir = DIRS[dir]
            dist = int(hex[:-1], 16)
            return (dir, dist)
        self.steps = [_parse(line) for line in lines]
