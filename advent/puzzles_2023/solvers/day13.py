from .base import Solver


class Day13(Solver):
    def parse(self, lines):
        def process(grid_lines):
            row_grid = [list(s) for s in grid_lines.split("\n")]
            col_grid = [list(seq) for seq in zip(*row_grid)]
            return row_grid, col_grid
        all = "\n".join(lines)
        self.grids = [process(gl) for gl in all.split("\n\n")]

    def reflects_at(self, items, index):
        scan_range = min(index, len(items) - index)
        for delta in range(0, scan_range):
            left = index - 1 - delta
            right = index + delta
            if items[left] != items[right]:
                return False
        return True
    
    def find_reflect_pos(self, items):
        for index in range(1, len(items)):
            if self.reflects_at(items, index):
                return index
        return None
    
    def score(self, row_refl, col_refl):
        if row_refl:
            return row_refl * 100
        else:
            return col_refl
    
    def find_refl_points(self, rows, cols):
        return tuple(self.find_reflect_pos(g) for g in (rows, cols))

class Day13Part1(Day13):
    def solve(self):
        return sum(
            self.score(*self.find_refl_points(rows, cols))
            for rows, cols in self.grids
        )


class Day13Part2(Day13):

    def toggle(self, rows, cols, r, c):
        rows[r][c] = opp(rows[r][c])
        cols[c][r] = opp(cols[c][r])

    def check(self, rows, cols):
        orig_points = self.find_refl_points(rows, cols)
        for r in range(len(rows)):
            for c in range(len(rows[0])):
                self.toggle(rows, cols, r, c)
                points = self.find_refl_points(rows, cols)
                if points != orig_points:
                    print(orig_points, "->", points)
                    return points
                self.toggle(rows, cols, r, c)
        assert False  # should not reach here

    def solve(self):
        return sum(
            self.score(*self.check(rows, cols))
            for rows, cols in self.grids
        )


def opp(sym):
    return "#" if sym == "." else "."