from util import input_lines


def day3_parse(file):
    return input_lines(file)


def priority(item):
    start, base = (ord("a"), 1) if item.islower() else (ord("A"), 27)
    return ord(item) - start + base


def day3_1(*packs):
    tot = 0
    for pack in packs:
        split = len(pack)//2
        left = set(pack[:split])
        right = set(pack[split:])
        shared = left.intersection(right).pop()
        tot += priority(shared)
    return tot


def day3_2(*packs):
    packgroups = (packs[i:i+3] for i in range(0, len(packs), 3))
    tot = 0
    for packgroup in packgroups:
        sets = [set(pack) for pack in packgroup]
        shared = sets[0].intersection(sets[1]).intersection(sets[2]).pop()
        tot += priority(shared)
    return tot
