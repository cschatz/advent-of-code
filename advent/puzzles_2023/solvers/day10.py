from .base import Solver


def _rev(dir):
    return tuple(-a for a in dir)


def _pipe(dirA, dirB):
    return {
        dirA: dirB,
        _rev(dirB): _rev(dirA),
    }


DIRS = ((-1, 0), (0, 1), (1, 0), (0, -1))
PIPES = {
    "|": _pipe((1, 0), (1, 0)),
    "-": _pipe((0, 1), (0, 1)),
    "L": _pipe((1, 0), (0, 1)),
    "J": _pipe((1, 0), (0, -1)),
    "7": _pipe((-1, 0), (0, -1)),
    "F": _pipe((-1, 0), (0, 1)),
    ".": {},
    "S": {},
}


class Day10(Solver):
    def parse(self, lines):
        self.num_rows = len(lines)
        self.num_cols = len(lines[0])
        self.start = None
        self.shapes = lines
        self.pipes = []
        for r, row in enumerate(lines):
            pipe_row = []
            for c, symbol in enumerate(row):
                if symbol == "S":
                    self.start = (r, c)
                pipe_row.append(PIPES[symbol])
            self.pipes.append(pipe_row)
        assert self.start is not None

                
    def in_bounds(self, r, c):
        return (
            r >= 0 and r < self.num_rows
            and c >= 0 and c < self.num_cols
        )
    
    def step(self, pos, dir):
        result = tuple(sum(x) for x in zip(pos, dir))
        return result if self.in_bounds(*result) else None
    
    def pipe_at(self, r, c):
        return self.pipes[r][c]
    
    def shape_at(self, r, c):
        return self.shapes[r][c]
    
    def follow_pipe(self, pos, in_dir):
        # return out dir when given pos pipe is entered with in_dir,
        # or None if not possible
        out_dir = self.pipe_at(*pos).get(in_dir)
        new_pos = None
        if out_dir:
            new_pos = self.step(pos, out_dir)
        return (new_pos, out_dir) if new_pos else (None, None)
    
    def extend_sequence(self, seq, last_in_dir):
        pos, dir = self.follow_pipe(seq[-1], last_in_dir)
        if pos is None:
            return None
        else:
            seq.append(pos)
            return dir
        
    def check_for_loop(self, start, initial_dir):
        second = self.step(start, initial_dir)
        if not second:
            return None
        seq = [start, second]
        dir = initial_dir
        while True:
            if seq[-1] == seq[0]:
                return seq
            dir = self.extend_sequence(seq, dir)
            if not dir:
                return None
            
    def find_loop(self):
         for initial_dir in DIRS:
            loop = self.check_for_loop(self.start, initial_dir)
            if loop:
                return loop        
        

class Day10Part1(Day10):
    def solve(self):
        return len(self.find_loop()) // 2
            

class Day10Part2(Day10):
    def solve(self):
        loop = set(self.find_loop())
        left = min(p[1] for p in loop)
        right = max(p[1] for p in loop)
        top = min(p[0] for p in loop)
        bottom = max(p[0] for p in loop)
        
        tiles = 0
        for r in range(top, bottom + 1):
            inside = False
            wall_start = None
            for c in range(left, right + 1):
                shape = self.shape_at(r, c)
                if (r, c) in loop:
                    if shape == "|":
                        inside = not inside
                    elif shape in "FL":
                        wall_start = shape
                    elif shape == "J":
                        if wall_start == "F":
                            inside = not inside
                        wall_start = None 
                    elif shape == "7":
                        if wall_start == "L":
                            inside = not inside
                        wall_start = None
                elif inside:
                    tiles += 1
        return tiles
