from functools import cmp_to_key, reduce
from operator import mul
from advent.util import input_all


def day13_parse(file):
    data = input_all(file).split("\n\n")
    pairs = [[eval(line) for line in pair.split("\n")] for pair in data]
    return pairs


def check(a, b):
    if type(a) == int and type(b) == int:
        return (a > b) - (a < b)
    a, b = [[x] if type(x) == int else x for x in (a, b)]
    if not (a or b):
        return 0
    if not b:
        return 1
    if not a:
        return -1
    comp_first = check(a[0], b[0])
    return comp_first if comp_first != 0 else check(a[1:], b[1:])


def day13_1(*pairs):
    return sum(i + 1 for i, p in enumerate(pairs) if check(*p) == -1)


def day13_2(*pairs):
    decoders = [[[2]], [[6]]]
    flattened = [x for pair in pairs for x in pair]
    all = flattened + decoders
    all.sort(key=cmp_to_key(check))
    return reduce(mul, (all.index(d) + 1 for d in decoders), 1)

