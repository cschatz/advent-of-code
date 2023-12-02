import sys

from .puzzle import Puzzle

from .util import (
    parse_args,
    SetupError,
)

try:
    puzzle = Puzzle(*parse_args(sys.argv))
    puzzle.solve()
except SetupError as e:
    print()
    print(f"*** {e}")
