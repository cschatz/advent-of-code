import re
import sys

from dataclasses import dataclass
from itertools import pairwise

from advent.solver_base import Solver


@dataclass
class Range:
    dst_start: int
    src_start: int
    rlen: int


class Map:
    def __init__(self, src_cat, dst_cat, ranges):
        self.src_cat = src_cat
        self.dst_cat = dst_cat
        self.ranges = sorted(ranges, key=lambda r: r.src_start)

    def map(self, src):
        for current, next in pairwise(self.ranges + [None]):
            rel = src - current.src_start
            if rel >= 0 and rel < current.rlen:
                return current.dst_start + rel
            elif next is not None and src < next.src_start:
                break
        return src


class Day5(Solver):
    def parse(self, lines):
        self.maps = []
        self.seeds = [int(s) for s in lines[0].replace("seeds: ", "").split(" ")]
        src, dst = None, None
        ranges = []
        for line in lines[2:] + [""]:
            if m := re.match(r"(\w+)-to-(\w+) map", line):
                src, dst = m.groups()
            elif line == "":
                # turns out src and dst categories aren't needed
                self.maps.append(Map(src, dst, ranges))
                ranges = []
            else:
                ranges.append(Range(*(int(x) for x in line.split(" "))))

    def seed_to_location(self, seed):
        n = seed
        for map in self.maps:
            n = map.map(n)
        return n


class Part1(Day5):

    def solve(self):
        return min(self.seed_to_location(s) for s in self.seeds)          


class Part2(Day5):
    def solve(self):
        s = self.seeds
        smallest = 1 << 64  # hopefully large enough!
        ranges = ((s[i], s[i+1]) for i in range(0, len(s), 2))
        for start, rlen in ranges:
            print(f"     Range {start} -> {start + rlen}")
            for rel in range(0, rlen):
                if rel % 1000000 == 0:
                    print(f"     ...{start + rel}")
                    sys.stdout.flush()
                loc = self.seed_to_location(start + rel)
                smallest = min(smallest, loc)
        return smallest
