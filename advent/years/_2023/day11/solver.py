from advent.solver_base import Solver


class Day11(Solver):
    SHIFT_FACTOR = 1

    def parse(self, lines):
        self.galaxies = []
        empty_rows = []
        nonempty_cols = set()
        num_rows = len(lines)
        num_cols = len(lines[0])
        for row, items in enumerate(lines):
            galaxy_cols = [c for c, item in enumerate(items) if item == "#"]
            if not galaxy_cols:
                empty_rows.append(row)
            for col in galaxy_cols:
                galaxy = (row, col)
                self.galaxies.append(galaxy)
                nonempty_cols.add(col)
        empty_cols = sorted(set(range(num_cols)) - nonempty_cols)
        self.row_adj = self._shift_amounts(empty_rows, num_rows)
        self.col_adj = self._shift_amounts(empty_cols, num_cols)

    def _shift_amounts(self, empties, length):
        empties = [0] + empties + [length]
        spans = [empties[i] - empties[i-1] for i in range(1, len(empties))]
        out = []
        for i, n in enumerate(spans):
            out.extend([i * self.SHIFT_FACTOR] * n)
        return out
    
    def solve(self):
        tot = 0
        for i, galaxy1 in enumerate(self.galaxies):
            for galaxy2 in self.galaxies[i + 1:]:
                tot += self.dist(galaxy1, galaxy2)
        return tot
    
    def adjust(self, row, col):
        return (row + self.row_adj[row], col + self.col_adj[col])

    def dist(self, g1, g2):
        return sum(
            abs(p[0] - p[1])
            for p in zip(self.adjust(*g1), self.adjust(*g2))
        )
    
                
class Part1(Day11):
    pass


class Part2(Day11):
    SHIFT_FACTOR = 999999





