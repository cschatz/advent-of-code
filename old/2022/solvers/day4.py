import re

from advent.util import input_lines


def day4_parse(file):
    return [map(int, (re.split(r'[,-]', line))) for line in input_lines(file)]


def day4_1(*ranges):
    def nested(a, b, c, d):
        return (a <= c and b >= d) or (b <= d and a >= c)
    return sum(map(lambda r: nested(*r), ranges))


def day4_2(*ranges):
    def overlapped(a, b, c, d):
        return (a <= c <= b) or (c <= a <= d)
    return sum(map(lambda r: overlapped(*r), ranges))
