from glob import glob
import sys

from .error import PuzzleError
from .util import (
    input_from_file,
    solver_class,
    validate_day_range,
    validate_part,
    validate_year,
)

DAY_PATH = "advent/years/_{}/day{}/"
INPUT_PATH = DAY_PATH + "inputs/"
PUZZLE_PATH = INPUT_PATH + "puzzle" 
TEST_PATH = INPUT_PATH + "test{}"


class Puzzle:
    def __init__(self, year, day, parts, include_puzzle, include_tests):
        self.parts = parts
        self.puzzle_solvers = []
        self.test_solvers = []
        for part in parts:
            solver_cls = solver_class(year, day, part)
            if include_puzzle:
                puzzle_input, _ = input_from_file(PUZZLE_PATH.format(year, day))
                self.puzzle_solvers.append(solver_cls(puzzle_input))
            if include_tests:
                files = glob(f"{TEST_PATH}*".format(year, day, part))
                if not files:
                    raise PuzzleError(f"Missing expected test input(s) for day {day} part {part}")
                part_test_solvers = []
                for filename in files:
                    test_input, expected = input_from_file(filename, is_test=True)
                    test_name = filename[len(TEST_PATH) + 1:].capitalize()
                    label = "Test" + (f" {test_name}" if test_name else "")
                    solver = solver_cls(test_input)
                    part_test_solvers.append((label, solver, expected))
                self.test_solvers.append(part_test_solvers)


    def solve(self):
        for i, part in enumerate(self.parts):
            print(f"\n  --- Part {part} ---")
            if self.test_solvers:
                for label, test_solver, expected in self.test_solvers[i]:
                    result = test_solver.solve()
                    msg = (
                        "pass" if str(result) == str(expected) else 
                        f"FAIL: {result} (expected {expected})"
                    )
                    print(f"  {label}: {msg}")
            if self.puzzle_solvers:
                result = self.puzzle_solvers[i].solve()
                print(f"  Solution: {result}")

    @staticmethod
    def _parse_args(args):
        if len(args) < 3:
            raise PuzzleError("Year and day required")
        year = validate_year(args[1])
        days = validate_day_range(args[2])
        other_digit = [a for a in args[3:] if a.isdigit()]
        if len(other_digit) > 1:
            raise PuzzleError("Too many numerical arguments")
        if other_digit:
            part = validate_part(other_digit[0])
            parts = (part,)
        else:
            parts = (1, 2)
        include_tests = "-p" not in args[3:]
        include_puzzle = "-t" not in args[3:]
        return (year, days, parts, include_puzzle, include_tests)


    @staticmethod
    def run_with_args(args):
        try:
            year, days, *other = Puzzle._parse_args(sys.argv)
            for day in days:
                puzzle = Puzzle(year, day, *other)
                print(f"======== Day {day} ========")
                puzzle.solve()
                print()
        except PuzzleError as e:
            print()
            print(f"*** {e}")

