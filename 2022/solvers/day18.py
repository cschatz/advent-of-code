from collections import defaultdict
from functools import cache
from util import input_lines

def day18_parse(file):
    largest = 0
    def parse(a):
        nonlocal largest
        x = int(a)
        largest = max(largest, x)
        return x
    coords = [tuple(parse(n) for n in line.split(",")) for line in input_lines(file)]
    return coords, largest

def f(p, n):
    k = p.index(None)
    return tuple(list(p[:k]) + [n] + list(p[k + 1:]))

def total_sides(cubes, n):
    sides = len(cubes) * 6
    spans = defaultdict(lambda: set())
    for x, y, z in cubes:
        spans[x, y, None].add(z)
        spans[x, None, z].add(y)
        spans[None, y, z].add(x)
    for st in spans.values():
        sides -= 2 * sum(all((i in st, i + 1 in st)) for i in range(n))
    return sides

def day18_1(cubes, n):
    return total_sides(cubes, n)

def day18_2(cubes, n):
    zeros = (0, 0, 0)
    dirs = [zeros[:i] + (x,) + zeros[i + 1:] for i in range(3) for x in (-1, 1)]
    cubes = set(cubes)
    outside = set()
    def in_bounds(p):
        return p not in cubes and all(x >= 0 and x <= n for x in p)
    def neighbors(p):
        return filter(
            in_bounds,
            (tuple(map(sum, zip(p, d))) for d in dirs)
        )
    def fill_outside(p):
        q = [p]
        outside.add(p)
        while q:
            curr = q.pop(0)
            for next in neighbors(curr):
                if next not in outside:
                    outside.add(next)
                    q.append(next)
    fill_outside((0, 0, 0))
    sides = total_sides(cubes, n)
    for pos in cubes:
        for adj in neighbors(pos):
            if adj not in outside:
                sides -= 1
    return sides
