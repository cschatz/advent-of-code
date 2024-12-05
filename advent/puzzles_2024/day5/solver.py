from collections import defaultdict
from ...solver import Solver

class Part1(Solver):
    def parse(self, lines):
        divider_pos = lines.index("")
        self.updates = [
            [int(x) for x in line.split(",")]
            for line in lines[divider_pos + 1:]
        ]   
        self.right_of = defaultdict(set)
        self.left_of = defaultdict(set)
        for line in lines[:divider_pos]:
            a, b = [int(x) for x in line.split("|")]
            self.right_of[a].add(b)
            self.left_of[b].add(a)

    def check_order(self, pages):
        seen = set([pages[0]])
        for page in pages[1:]:
            not_left = self.right_of[page]
            if any(p in seen for p in not_left):
                return False
            seen.add(page)
        return True

    def solve(self):
        tot = 0
        for pages in self.updates:
            if self.check_order(pages):
                tot += pages[len(pages) // 2]
        return tot

class Part2(Part1):
    def find_middle(self, pages):
        num_pages = len(pages)
        page_set = set(pages)
        for page in pages:
            pos = num_pages - 1 - len(self.right_of[page].intersection(page_set))
            if pos == num_pages // 2:
                return page

    def solve(self):
        tot = 0
        for pages in self.updates:
            if not self.check_order(pages):
                tot += self.find_middle(pages)
        return tot