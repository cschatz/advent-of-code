from .base import Solver

from math import lcm


class Day8(Solver):
    def parse(self, lines):
        self.instructions = lines[0]
        self.num_instructions = len(self.instructions)
        self.nodes = {}
        for line in lines[2:]:
            self.nodes[line[0:3]] = (line[7:10], line[12:15])

    def step(self, label, direction):
        return self.nodes[label][0 if direction == "L" else 1]
    
    def count_steps(self, start_label, check_end):
        current = start_label
        steps = 0
        while not check_end(current):
            current = self.step(current, self.instructions[steps % self.num_instructions])
            steps += 1
        return steps
        

class Day8Part1(Day8):
    def solve(self):
        return self.count_steps("AAA", lambda n: n == "ZZZ")


class Day8Part2(Day8):
    def solve(self):
        return lcm(
            *(
                self.count_steps(label, lambda n: n[2] == "Z")
                for label in self.nodes.keys() if label[2] == "A"
            )
        )