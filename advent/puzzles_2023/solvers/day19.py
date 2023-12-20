import re

from functools import reduce
from operator import __mul__

from .base import Solver


class Condition:
    def __init__(self, text):
        self.text = text
        self.cat = text[0]
        self.op = text[1]
        self.value = int(text[2:])
        if self.op == "<":
            self.predicate = lambda p: p[self.cat] < self.value
        else:
            self.predicate = lambda p: p[self.cat] > self.value

    def apply(self, part):
        return self.predicate(part)
    
    def __str__(self):
        return self.text


class Rule:
    def __init__(self, text, terminal=False):
        if terminal:
            self.condition = None
            self.target = text
        else:
            cond, self.target = text.split(":")
            self.condition = Condition(cond)

    def apply(self, part):
        if not self.condition:
            return self.target
        else:
            return self.target if self.condition.apply(part) else None

    def __str__(self):
        if self.condition:
            return f"({self.condition}) -> {self.target}"
        else:
            return f"* -> {self.target}"
       


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
    def trace_paths(self, name, constraints):
        for rule in self.workflows[name]:
            if rule.condition is None:  # terminal output
                constraints_on_true = constraints
            else:
                constraints_on_true = _updated_constraints(constraints, rule.condition)
                constraints = _updated_constraints(constraints, _invert(rule.condition))
            if constraints_on_true is not None:
                if rule.target == "A":
                    yield constraints_on_true
                elif rule.target != "R":
                    yield from self.trace_paths(rule.target, constraints_on_true)

    def solve(self):
        paths = self.trace_paths("in", {c: (1, 4000) for c in "xmas"})
        return sum(
            reduce(
                __mul__,
                (upper - lower + 1 for lower, upper in path.values()) 
            )
            for path in paths
        )

def _updated_constraints(constraints, cond):
    lower, upper = constraints.get(cond.cat, (1, 4000))
    if cond.op == '>':
        if cond.value >= upper:
            return None
        lower = cond.value + 1
    else:
        if cond.value <= lower:
            return None
        upper = cond.value - 1
    return dict(constraints, **{cond.cat: (lower, upper)})


def _parse_rating_set(text):
    ratings = text[1:-1].split(",")
    return {rating[0]: int(rating[2:]) for rating in ratings}


def _parse_workflow(text):
    m = re.match(r"(.+)\{(.+)\}", text)
    label = m.group(1)
    rules = m.group(2).split(",")
    steps = tuple(Rule(r) for r in rules[:-1])
    steps = steps + (Rule(rules[-1], terminal=True),)
    return {label: steps}


def _apply_workflow(workflow, part):
    for condition in workflow:
        result = condition.apply(part)
        if result:
            return result


def _score(part):
    return sum(part.values())


def _invert(cond):
    inv_cond = cond
    if cond.op == ">":
        inv_cond.op = "<"
        inv_cond.value = cond.value + 1
    else:
        inv_cond.op = ">"
        inv_cond.value = cond.value - 1
    return inv_cond
