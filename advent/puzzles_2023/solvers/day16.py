from dataclasses import dataclass

from .base import Solver


@dataclass(frozen=True)
class Vector:
    x: int
    y: int


@dataclass(frozen=True)
class Beam:
    pos: Vector
    vel: Vector


def advance(pos, vel):
    return Vector(pos.x + vel.x, pos.y + vel.y)


def dot(beam):
    # continue in same direction
    return [Beam(advance(beam.pos, beam.vel), beam.vel)]


def _diag(beam, sign):
    if beam.vel.y == 0:  #  from right or left
        new_vel = Vector(0, sign * beam.vel.x)
    else:
        new_vel = Vector(sign * beam.vel.y, 0)
    return [Beam(advance(beam.pos, new_vel), new_vel)]


def slash(beam):
    return _diag(beam, -1)


def backslash(beam):
    return _diag(beam, 1)


def splitter_vert(beam):
    if beam.vel.x == 0:
        return dot(beam)
    else:
        return [
            Beam(advance(beam.pos, vel), vel)
            for vel in (Vector(0, -1), Vector(0, 1))
        ]


def splitter_horiz(beam):
    if beam.vel.y == 0:
        return dot(beam)
    else:
        return [
            Beam(advance(beam.pos, vel), vel)
            for vel in (Vector(-1, 0), Vector(1, 0))
        ]


ACTIONS = {
    ".": dot,
    "/": slash,
    "\\": backslash,
    "-": splitter_horiz,
    "|": splitter_vert,
}


class Day16(Solver):
    def parse(self, lines):
        self.grid = lines
        self.num_rows = len(lines)
        self.num_cols = len(lines[0])

    def in_bounds(self, beam):
        return (
            beam.pos.x >= 0 and beam.pos.x < self.num_cols
            and beam.pos.y >= 0 and beam.pos.y < self.num_rows
        )
    
    def tiles_energized(self, start):
        beams = [start]
        history = set([start])
        visited = set([start.pos])
        while beams:
            current = beams.pop()
            object = self.grid[current.pos.y][current.pos.x]
            next_beams = ACTIONS[object](current)
            for b in next_beams:
                if self.in_bounds(b) and b not in history:
                    beams.append(b)
                    history.add(b)
                    visited.add(b.pos)
        return len(visited)


class Day16Part1(Day16):
    def solve(self):
        return self.tiles_energized(Beam(Vector(0, 0), Vector(1, 0)))
        
 

class Day16Part2(Day16):
    def solve(self):
        starts = []
        for x in range(self.num_cols):
            starts.append(Beam(Vector(x, 0), Vector(0, 1)))
            starts.append(Beam(Vector(x, self.num_rows - 1), Vector(0, -1)))
        for y in range(self.num_rows):
            starts.append(Beam(Vector(0, y), Vector(1, 0)))
            starts.append(Beam(Vector(0, self.num_cols - 1), Vector(-1, 0)))
        return max(
            self.tiles_energized(start)
            for start in starts
        )



