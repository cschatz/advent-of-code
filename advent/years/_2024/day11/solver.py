from functools import cache

from advent.solver_base import Solver

@cache
def blink(stone, n):
    if n == 0:
        return 1
    if stone == 0:
        return blink(1, n - 1)
    if (digits := len(rock := str(stone))) % 2 == 0:
        half = digits // 2
        return (
            blink(int(rock[:half]), n - 1)
            + blink(int(rock[half:]), n - 1)
        )
    return blink(stone * 2024, n - 1)

class Part1(Solver):
    def parse(self, lines):
        self.stones = [int(x) for x in lines[0].split(" ")]

    def do_blinks(self, num_blinks):
        return sum(blink(stone, num_blinks) for stone in self.stones)
    
    def solve(self):
        return self.do_blinks(25)

class Part2(Part1):
    def solve(self):
        return self.do_blinks(75)