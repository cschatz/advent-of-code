from bisect import insort
from collections import defaultdict
import re
from util import input_lines

def smart(fn):
    return lambda a, b: b if a is None else fn(a, b)


smartmin = smart(min)
smartmax = smart(max)

def day15_parse(file):
    def parse(line):
        ns = tuple(int(a) for a in re.findall(r'=(-?\d+)', line))
        return (ns[:2], ns[2:])
    return [parse(line) for line in input_lines(file)]

def merge_in(intervals, new):
    if len(intervals) == 0:
        intervals.append(new)
        return
    old = intervals[:]
    insort(old, new, key=lambda x: x[0])
    intervals.clear()
    intervals.append(old[0])
    for interval in old[1:]:
        if interval[0] <= intervals[-1][1] + 1:
            intervals[-1][1] = max(intervals[-1][1], interval[1])
        else:
            intervals.append(interval)

def manhattan_distance(sensor, beacon):
    return sum(abs(x - y) for x, y in zip(sensor, beacon))

def impacts_in_row(sensor_x, d, left_bound=None, right_bound=None,
                   beacon_x_in_row=None):
    assert d >= 0
    left = smartmax(left_bound, sensor_x - d)
    right = smartmin(right_bound, sensor_x + d)
    if beacon_x_in_row is None:
        return [[left, right]]
    else:
        return [[left, beacon_x_in_row - 1], [beacon_x_in_row + 1, right]]


def day15_1(*signals):
    nope = []
    row = 2000000
    # row = 10
    for sensor, beacon in signals:
        d = manhattan_distance(sensor, beacon) - abs(sensor[1] - row)
        if d >= 0:
            spans = impacts_in_row(
                sensor[0], d,
                beacon_x_in_row=beacon[0] if beacon[1] == row else None
            )
            for span in spans:
                merge_in(nope, span)
    return sum(b - a + 1 for a, b in nope)

def day15_2(*signals):
    MAX_ROW = 4000000
    row_impacts = defaultdict(lambda: [])
    rows_ruled_out = set()
    for sensor, beacon in signals:
        sensor_x, sensor_y = sensor
        md = manhattan_distance(sensor, beacon)
        print(f"{len(rows_ruled_out)} ruled out")
        for r, d in ((sensor_y + d, md - abs(d)) for d in range(-md, md + 1)):
            if r >= 0 and r <= MAX_ROW and r not in rows_ruled_out:
                spans = impacts_in_row(sensor_x, d, left_bound=0, right_bound=MAX_ROW)
                for span in spans:
                    merge_in(row_impacts[r], span)
                    if len(row_impacts[r]) == 1 and row_impacts[r][0] == [0, MAX_ROW]:
                        rows_ruled_out.add(r)
                        del row_impacts[r]
                        break
    row = list(row_impacts.keys())[0]
    intervals = list(row_impacts.values())[0]
    return (intervals[0][1] + 1) * MAX_ROW + row
