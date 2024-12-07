import re

from ...solver_base import Solver


class Part1(Solver):
    def solve(self):
        return sum(
            sum(int(a) * int(b) for a, b in re.findall(r'mul\((\d+),(\d+)\)', line))
            for line in self.lines
        )
    

class Part2(Part1):
    def solve(self):
        tot = 0
        enabled = True
        for line in self.lines:
            matches = re.findall(r'mul\((\d+),(\d+)\)|(do\(\))|(don\'t\(\))', line)
            for match in matches:
                a, b, do, dont = match
                if enabled and a:
                    tot += int(a) * int(b)
                elif do:
                    enabled = True
                elif dont:
                    enabled = False
        return tot