from collections import namedtuple
from functools import reduce
from math import lcm
from operator import mul
from re import split
from advent.util import input_all

Monkey = namedtuple('Monkey', ['items', 'op', 'next', 'divisor'])


def day11_parse(file):
    pattern = r"s: |w = |by |y "
    def parse(chunk):
        specs = [split(pattern, x)[1] for x in chunk.split("\n")[1:]]
        return monkey(*specs)
    def monkey(items, op, div, yes, no):
        return Monkey(
            [int(x) for x in items.split(", ")],
            eval(f"lambda old: {op}"),
            lambda x: int(yes) if x % int(div) == 0 else int(no),
            int(div)
        )
    return [parse(c) for c in input_all(file).split("\n\n")]


def day11(*monkeys, rounds, worry_drop):
    counts = [0] * len(monkeys)
    base = reduce(mul, (m.divisor for m in monkeys), 1)
    def round():
        for i in range(len(monkeys)):
            counts[i] += len(monkeys[i].items)
            for w in monkeys[i].items:
                w = monkeys[i].op(w)
                w = w // worry_drop
                next = monkeys[i].next(w)
                monkeys[next].items.append(w % base)
            monkeys[i].items.clear()
    for r in range(rounds):
        round()
    return reduce(mul, sorted(counts)[-2:], 1)


def day11_1(*monkeys):
    return day11(*monkeys, rounds=20, worry_drop=3)


def day11_2(*monkeys):
    return day11(*monkeys, rounds=10000, worry_drop=1)
