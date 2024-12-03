from ...solver import Solver

class Day1Part1(Solver):

    def parse(self, lines):
        def process(line):
            return tuple(int(x) for x in line.split())
        self.lists = zip(*[process(line) for line in lines])

    def solve(self):
        return sum(
            abs(a - b)
            for a, b in zip(*map(sorted, self.lists))
        )

class Day1Part2(Day1Part1):
    def solve(self):
        left, right = self.lists
        return sum(
            n * left.count(n)
            for n in right
        )
