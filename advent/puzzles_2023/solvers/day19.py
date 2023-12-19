import re

from .base import Solver


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
        ...


def _parse_rating_set(text):
    ratings = text[1:-1].split(",")
    return {rating[0]: int(rating[2:]) for rating in ratings}


def _parse_workflow(text):
    m = re.match(r"(.+)\{(.+)\}", text)
    label = m.group(1)
    rules = m.group(2).split(",")
    steps = tuple(_parse_rule(r) for r in rules[:-1])
    steps = steps + (_parse_rule(rules[-1], last_rule=True),)
    return {label: steps}


def _parse_rule(text, last_rule=False):
    if last_rule:
        return lambda _: text
    else:
        condition, label = text.split(":")
        category = condition[0]
        comparison = condition[1]
        cutoff = int(condition[2:])
        if comparison == "<":
            return lambda part: label if part[category] < cutoff else None
        else:
            return lambda part: label if part[category] > cutoff else None


def _apply_workflow(workflow, part):
    for rule in workflow:
        result = rule(part)
        if result is not None:
            return result


def _score(part):
    return sum(part.values())
