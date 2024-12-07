from operator import add
from advent.util import input_lines
from functools import reduce


def day7_parse(file):
    return input_lines(file)


def build(input):
    root = [None, {}, 0]
    cur = root
    for line in input:
        if line[:4] == "$ cd":
            dir = line[5:]
            if dir == "/":
                cur = root
            elif dir == "..":
                cur = cur[0]
            else:
                subdir = [cur, {}, 0]
                cur[1][dir] = subdir
                cur = subdir
        elif (s := line.split()[0]).isnumeric():
            cur[2] += int(s)
    return root


def size_data(root):
    def s(node):
        tots, lsts = tuple(zip(*[s(n) for n in node[1].values()])) or ([], [])
        tot = sum(tots) + node[2]
        lst = reduce(add, lsts, []) + [tot]
        return tot, lst
    return s(root)


def day7_1(*input):
    dirs = size_data(build(input))[1]
    return(sum(s for s in dirs if s <= 100000))


def day7_2(*input):
    all, dirs = size_data(build(input))
    return(min(s for s in dirs if all - s <= 40000000))
