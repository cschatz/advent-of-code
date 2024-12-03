import re

from ...solver import Solver

def mul(a, b, *_):
    return int(a) * int(b)

class Part1(Solver):
    def solve(self):
        tot = 0
        for line in self.lines:
            matches = re.findall(r'mul\((\d+),(\d+)\)', line)
            tot += sum(mul(*match) for match in matches)
        return tot
    
    

class Part2(Part1):
    def solve(self):
        tot = 0
        do = True
        for line in self.lines:
            matches = re.findall(r'mul\((\d+),(\d+)\)|(do\(\))|(don\'t\(\))', line)
            for match in matches:
                if match[0] and do:
                    tot += mul(*match)
                elif match[2]:
                    do = True
                elif match[3]:
                    do = False
        return tot