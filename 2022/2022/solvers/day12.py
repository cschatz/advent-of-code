from util import input_lines


DIRS = ((-1, 0), (0, 1), (1, 0), (0, -1))


class Heightmap:
    def __init__(self, grid, start, end):
        self.grid = grid
        self.start = start
        self.end = end
        self.rows = len(grid)
        self.cols = len(grid[0])

    def __getitem__(self, p):
        return self.grid[p[0]][p[1]]

    def in_grid(self, p):
        r, c = p
        return all((r >= 0, c >= 0, r < self.rows, c < self.cols))

    def bfs(self, start, goalcheck, passable):
        seen = set([start])
        def neighbors(p, passable):
            return (
                n for n in (tuple(sum(x) for x in zip(p, d)) for d in DIRS)
                if self.in_grid(n) and n not in seen and passable(self[p], self[n])
            )
        open = [(start, 0)]
        while len(open) > 0:
            current, cost = open.pop(0)
            if goalcheck(current):
                return cost
            for s in neighbors(current, passable):
                seen.add(s)
                open.append((s, cost + 1))
        return -1

    def best_path_up(self):
        return self.bfs(
            self.start, lambda p: p == self.end, lambda a, b: b <= a + 1)

    def best_path_down(self):
        return self.bfs(
            self.end, lambda p: self[p] == 0, lambda a, b: a <= b + 1)


def day12_parse(file):
    endpoints = [None, None]
    def p(r, c, x):
        if x == "S":
            endpoints[0] = (r, c)
            x = "a"
        elif x == "E":
            endpoints[1] = (r, c)
            x = "z"
        return ord(x) - ord("a")
    rows = input_lines(file)
    grid = [
        [p(r, c, x) for c, x in enumerate(row)] for r, row in enumerate(rows)
    ]
    return [Heightmap(grid, *endpoints)]


def day12_1(hm):
    return hm.best_path_up()


def day12_2(hm):
    return hm.best_path_down()
