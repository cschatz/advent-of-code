from advent.solver_base import Solver


CARDINAL = ((0, 1), (0, -1), (1, 0), (-1, 0))


class Day21(Solver):
    def parse(self, lines):
        self.grid = lines
        self.height = len(lines)
        self.width = len(lines[0])
        find_start = (
            (r, c)
            for r, row in enumerate(lines)
            for c, x in enumerate(row)
            if x == "S"
        )
        self.start = next(find_start)

    def in_bounds(self, r, c):
        return r >= 0 and r < self.height and c >= 0 and c < self.width
    
    def neighbors(self, r, c, omit):
        candidates = ((r + dr, c + dc) for dr, dc in CARDINAL)
        return (
            (rr, cc) for rr, cc in candidates
            if self.in_bounds(rr, cc)
            and (rr, cc) not in omit
            and self.grid[rr][cc] != "#"
        )
    

class Part1(Day21):
    def plots_reachable(self, tot_steps):
        visited = set()
        reachable = set()
        q = [(self.start, tot_steps)]
        while q:
            pos, steps_left = q.pop(0)
            if pos in visited:
                continue
            visited.add(pos)
            if steps_left % 2 == 0:
                reachable.add(pos)
            if steps_left > 0:
                for p in self.neighbors(*pos, visited):
                    q.append((p, steps_left - 1))
        return len(reachable)

    def solve(self):
        if self.width < 20:  # test
            return self.plots_reachable(6)
        else:
            return self.plots_reachable(64)

class Part2(Day21):
    ...