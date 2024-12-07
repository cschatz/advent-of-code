from collections import defaultdict
from ...solver_base import Solver

class Part1(Solver):
    def parse(self, lines):
        divider_pos = lines.index("")
        self.updates = [line.split(",") for line in lines[divider_pos + 1:]]   
        self.right_of = defaultdict(set)
        for line in lines[:divider_pos]:
            a, b = line.split("|")
            self.right_of[a].add(b)

    def check_order(self, pages):
        seen = set()
        for page in pages:
            if self.right_of[page].intersection(seen): # non-empty?
                return False
            seen.add(page)
        return True

    def solve(self):
        return sum(
            int(pages[len(pages) // 2])
            for pages in self.updates
            if self.check_order(pages)
        )

class Part2(Part1):
    def find_middle(self, pages):
        def check(p):
            return (
                len(pages) - len(self.right_of[p].intersection(pages))
                == len(pages) // 2 + 1
            )
        # first(only) item from generator expr
        return next(filter(check, pages))

    def solve(self):
        return sum(
            int(self.find_middle(pages))
            for pages in self.updates
            if not self.check_order(pages)
        )
