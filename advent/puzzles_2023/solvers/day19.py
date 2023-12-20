import re

from .base import Solver


class Condition:
    def __init__(self, text, terminal=False):
        self.text = text
        self.key = None
        self.op = None
        self.target = None
        if terminal:
            self.predicate = None
            self.target = text
        else:
            condition, self.target = text.split(":")
            self.key = condition[0]
            self.op = condition[1]
            self.value = int(condition[2:])
            if self.op == "<":
                self.predicate = lambda p: p[self.key] < self.value
            else:
                self.predicate = lambda p: p[self.key] > self.value

    def apply(self, part):
        if self.predicate:
            return self.target if self.predicate(part) else None
        else:
            return self.target

    def __repr__(self):
        return (self.key, self.op, self.value, self.target)


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
    def check_part(self, part):
        workflow = self.workflows["in"]
        while True:
            out = _apply_workflow(workflow, part)
            if out in ("A", "R"):
                return out == "A"
            else:
                workflow = self.workflows[out]

    def solve(self):
        return sum(
            _score(part)
            for part in self.parts
            if self.check_part(part)
        )


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
        result = condition.apply(part)
        if result:
            return result


def _score(part):
    return sum(part.values())


def _opp(comparison, cutoff):
    if comparison == "<":
        return (">", cutoff - 1)
    else:
        return ("<", cutoff + 1)
