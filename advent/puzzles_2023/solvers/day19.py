import re

from .base import Solver


class Condition:
    def __init__(self, text, terminal=False):
        self.text = text
        if terminal:
            self.check = None
            self.value = text
        else:
            condition, self.value = text.split(":")
            self.category = condition[0]
            self.comparison = condition[1]
            self.cutoff = int(condition[2:])
            if self.comparison == "<":
                self.check = lambda p: p[self.category] < self.cutoff
            else:
                self.check = lambda p: p[self.category] > self.cutoff

    def __call__(self, part):
        if self.check:
            return self.value if self.check(part) else None
        else:
            return self.value

    def split(self):
        return (
            self.category,
            (self.comparison, self.cutoff),
            self.value,
            _opp(self.comparison, self.cutoff)
        )


class Day19(Solver):
    def parse(self, lines):
        all = "\n".join(lines)
        workflows, parts = all.split("\n\n")

        self.parts = [
            _parse_rating_set(rating_set)
            for rating_set in parts.split("\n")
        ]
        self.workflows = {}
        for workflow in workflows.split("\n"):
            self.workflows.update(_parse_workflow(workflow))


class Day19Part1(Day19):
    def eval_part(self, part):
        workflow = self.workflows["in"]
        while True:
            out = _apply_workflow(workflow, part)
            if out in ("A", "R"):
                return out
            else:
                workflow = self.workflows[out]

    def solve(self):
        tot = 0
        for part in self.parts:
            if self.eval_part(part) == "A":
                tot += _score(part)
        return tot


class Day19Part2(Day19):
    def solve(self):
        workflow = self.workflows["in"]
        


def _parse_rating_set(text):
    ratings = text[1:-1].split(",")
    return {rating[0]: int(rating[2:]) for rating in ratings}


def _parse_workflow(text):
    m = re.match(r"(.+)\{(.+)\}", text)
    label = m.group(1)
    rules = m.group(2).split(",")
    steps = tuple(Condition(r) for r in rules[:-1])
    steps = steps + (Condition(rules[-1], terminal=True),)
    return {label: steps}


def _apply_workflow(workflow, part):
    for condition in workflow:
        result = condition(part)
        if result:
            return result


def _score(part):
    return sum(part.values())


def _opp(comparison, cutoff):
    if comparison == "<":
        return (">", cutoff - 1)
    else:
        return ("<", cutoff + 1)
