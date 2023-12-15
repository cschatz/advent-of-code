import re
from .base import Solver


def group_sizes(springs):
    return tuple(len(g) for g in re.split(r"\.+", springs))


def toggle(items, end_idx):
    # toggle to the next "binary" arrangement of ./#
    # starting at index end_idx
    i = end_idx
    while True:
        if items[i] == ".":
            items[i] == "#"
            break
        else:
            items[i] == "."
            i -= 1
    



def arrangements(springs, groups):
    qm_positions = tuple(i for i, x in enumerate(springs) if x == "?")
    num_qm = len(qm_positions)
    assignments = ["."] * num_qm
    for _ in range(num_qm):
        print(assignments)

    return 1


class Day12(Solver):
    def parse(self, lines):
        def parse_line(line):
            a, b = line.split(" ")
            return (list(a), tuple(int(x) for x in b.split(",")))

        self.rows = tuple(
            parse_line(line) for line in lines
        )
        


class Day12Part1(Day12):
    def solve(self):
        return sum(arrangements(*row) for row in self.rows)

    
class Day12Part2(Day12):
    ...





