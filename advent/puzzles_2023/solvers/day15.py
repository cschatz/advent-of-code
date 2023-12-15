import re

from .base import Solver

from collections import defaultdict

class Day15(Solver):
    def parse(self, lines):
        all = ''.join(lines)
        self.steps = all.split(",")

    def hash(self, text):
        n = 0
        for c in text:
            n = ((n + ord(c)) * 17) % 256
        return n



class Day15Part1(Day15):
    def solve(self):
        return sum(self.hash(s) for s in self.steps)

    
class Day15Part2(Day15):
    def remove(self, lenses, label):
        num_lenses = len(lenses)
        i = 0
        while i < num_lenses and lenses[i][0] != label:
            i += 1
        for j in range(i + 1, num_lenses):
            lenses[j - 1] = lenses[j]
        if i < num_lenses:
            lenses.pop()

    def insert_or_swap(self, lenses, label, foclen):
        for lens in lenses:
            if lens[0] == label:
                lens[1] = foclen
                break
        else:
            lenses.append([label, foclen])

    def solve(self):
        boxes = defaultdict(list)
        for step in self.steps:
            m = re.match(r"([a-z]+)(-|=)(\d*)", step)
            label, action, foclen = m.groups()
            box = self.hash(label)
            if action == "-":
                self.remove(boxes[box], label)
            else:
                self.insert_or_swap(boxes[box], label, int(foclen))
        return (
            sum(
                (b + 1) * sum((i + 1) * x[1] for i, x in enumerate(boxes[b]))
                for b in range(256)
            )
        )
