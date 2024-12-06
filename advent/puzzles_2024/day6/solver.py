from collections import defaultdict
from ...solver import Solver

UP_DIR = (-1, 0)
START_UP = "^"
OBSTACLE = "#"
OPEN = "."

def right_90(dr, dc):
    return (dc, -dr)


def vadd(vecA, vecB):
    return tuple(map(sum, zip(vecA, vecB)))


class Part1(Solver):
    def in_bounds(self, r, c):
        return all((r >= 0, c >= 0, r < self.rows, c < self.cols))
    
    def get(self, r, c):
        return self.grid[r][c]
    
    def set(self, r, c, val):
        self.grid[r][c] = val

    def parse(self, lines):
        self.grid = [list(line) for line in lines]
        self.rows = len(lines)
        self.cols = len(lines[0])
        self.start_pos = next(
            (r, c)
            for r, line in enumerate(lines)
            for c, cell in enumerate(line)
            if cell == START_UP
        )
        
        
    def guard_path(self):
        # returns (path_length, is_loop, path_locs)
        visited = set()
        visited_locs = set()
        pos, dir = (self.start_pos, UP_DIR)
        visited = set()
        while True:
            visited_locs.add(pos)
            visited.add((pos, dir))
            next_pos = vadd(pos, dir)
            if not self.in_bounds(*next_pos):
                return len(visited_locs), False, visited_locs
            elif (next_pos, dir) in visited:
                return len(visited_locs), True, visited_locs
            if self.get(*next_pos) == OBSTACLE:
                dir = right_90(*dir)
            else:
                pos = next_pos
        
    def solve(self):
        path_length, _, _ = self.guard_path()
        return path_length


class Part2(Part1):
    def solve(self):
        _, _, orig_path = self.guard_path()
        count = 0
        to_check = [
            (r, c)
            for r in range(self.rows)
            for c in range(self.cols)
            if (r, c) in orig_path and self.get(r, c) == OPEN
        ]
        for r, c in to_check:
            self.set(r, c, OBSTACLE)
            _, causes_loop, _ = self.guard_path()
            if causes_loop:
                count += 1
            self.set(r, c, OPEN)

        
        # for r in range(self.rows):
        #     for c in range(self.cols):
        #         if self.get(r, c) == OPEN:
        #             self.set(r, c, OBSTACLE)
        #             _, causes_loop, _ = self.guard_path()
        #             if causes_loop:
        #                 count += 1
        #             self.set(r, c, OPEN)
        return count
