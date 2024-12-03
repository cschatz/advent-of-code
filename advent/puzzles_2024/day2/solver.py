import re

from ...solver import Solver

DIGIT_WORDS = (
    "one", "two", "three", "four", "five", "six", "seven", "eight", "nine")


class Day2Part1(Solver):

    def parse(self, lines):
        self.reports = [
            [int(x) for x in line.split(" ")]
            for line in lines
        ]
        def process(line):
            return tuple(int(x) for x in line.split())
        self.lists = zip(*[process(line) for line in lines])

    def check_report(self, report):
        n = len(report)
        steps = [report[i+1] - report[i] for i in range(n-1)]
        increasing = steps[0] > 0
        for step in steps:
            if step == 0:
                return False
            if (step > 0) != increasing:
                return False
            size = abs(step)
            if size < 1 or size > 3:
                return False
        return True

    def solve(self):
        return sum(self.check_report(report) for report in self.reports)
    

class Day2Part2(Day2Part1):

    def check_report(self, report):
        if super().check_report(report):
            return True
        n = len(report)
        for dampened_report in [report[:i] + report[i+1:] for i in range(n)]:
            if super().check_report(dampened_report):
                return True
        return False