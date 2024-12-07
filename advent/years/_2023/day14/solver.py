import re

from advent.solver_base import Solver

from collections import defaultdict

class Day14(Solver):
    def parse(self, lines):
        self.cols = [list(c) for c in zip(*lines)]

    def load(self, col):
        colsize = len(col)
        i = 0
        tot_load = 0
        while True:
            if i == colsize:
                break
            # find beginning of open space or rocks
            while i < colsize and col[i] == "#":
                i += 1
            # count all Os until end or "#"
            one_rock_load = len(col) - i
            while i < colsize and col[i] != "#":
                if col[i] == "O":
                    tot_load += one_rock_load
                    one_rock_load -= 1
                i += 1
        return tot_load        

class Part1(Day14):
    def solve(self):
        return sum(self.load(col) for col in self.cols)
 
class Part2(Day14):
    def solve(self):
        ...