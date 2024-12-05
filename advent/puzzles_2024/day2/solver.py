import re

from ...solver import Solver


class Part1(Solver):
    def parse(self, lines):
        self.reports = [
            [int(x) for x in line.split(" ")]
            for line in lines
        ]

    def check_report(self, report):
        steps = [report[i+1] - report[i] for i in range(len(report)-1)]
        increasing = steps[0] > 0
        for step in steps:
            size = abs(step)
            if step == 0 or ((step > 0) != increasing) or size < 1 or size > 3:
                return False
        return True

    def solve(self):
        return sum(self.check_report(report) for report in self.reports)
    

class Part2(Part1):
    def check_report(self, report):
        check = super().check_report
        return any(
            check(dampened_report)
            for dampened_report in [report[:i] + report[i+1:] for i in range(len(report))]
        )