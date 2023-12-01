from functools import reduce
from operator import add, sub
from util import input_lines


def day9_parse(file):
    return (line.split(" ") for line in input_lines(file))


def day9(*s, n=1):
    a = dict(zip("RLUD", [(1, 0), (-1, 0), (0, 1), (0, -1)]))
    r = list(map(lambda _: [0, 0], range(n+1)))
    v = set()
    for m in (a[c] for c, nm in s for _ in range(int(nm))):
        r[0] = list(map(add, r[0], m))
        for h, t in (r[i:i+2] for i in range(n)):
            g = tuple(map(sub, h, t))
            if 2 in map(abs, g):
                t[:] = map(lambda k, d: t[k] + d//(abs(d) or 1), range(2), g)
        v.add(tuple(r[-1]))
    return len(v)


def day9_1(*s):
    return day9(*s)


def day9_2(*s):
    return day9(*s, n=9)
