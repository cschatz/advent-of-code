from advent.util import input_all


def day1_parse(file):
    elves = input_all(file).split("\n\n")
    return [[int(line) for line in elf.split("\n")] for elf in elves]


def day1_1(*data):
    return max(sum(chunk) for chunk in data)


def day1_2(*data):
    return sum(sorted([sum(chunk) for chunk in data])[-3:])
