import sys

from .argparsing import parse_args
from .puzzle import Puzzle, PuzzleError

try:
    year, days, *other = parse_args(sys.argv)
    for day in days:
        puzzle = Puzzle(year, day, *other)
        print(f"==== Day {day} ====")
        puzzle.solve()
        print()
except PuzzleError as e:
    print()
    print(f"*** {e}")