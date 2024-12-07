from advent.solver_base import Solver


class Part1(Solver):
    def parse(self, lines):
        self.equations = [
            [int(left), right.split(" ")]
            for left, right in ((line.split(": ")) for line in lines)
        ]
        
    def can_work(self, value, target, terms):
        if value > target:
            return False
        if len(terms) == 0:
            return value == target
        return any((
            self.can_work(value + int(terms[0]), target, terms[1:]),
            self.can_work(value * int(terms[0]), target, terms[1:])
        ))
    
    def solve(self):
        return sum(
            target
            for target, terms in self.equations
            if self.can_work(0, target, terms)
        )


class Part2(Part1):
    def can_work(self, value, target, terms):
        if value > target:
            return False
        if len(terms) == 0:
            return value == target
        return any((
            self.can_work(value + int(terms[0]), target, terms[1:]),
            self.can_work(value * int(terms[0]), target, terms[1:]),
            self.can_work(int(str(value) + terms[0]), target, terms[1:]),
        ))