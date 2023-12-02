from glob import glob
from importlib import import_module
from sys import argv

from solvers.base import TestFailure

INPUTS = "inputs"
SOLVERS = "solvers"
EXPECTED_MARKER = ":"


class SetupError(Exception):
    pass


class Puzzle:
    """Represent applying solver code to a particular day's puzzle,
    optionally including test input in addition to the main puzzle input."""

    def __init__(self, day, parts, skip_tests):
        self.day = day
        self.parts = parts
        self.skip_tests = skip_tests
        self.solver = None
        self.inputs = {}
        self._instantiate_solver()
        self._collect_inputs()

    @classmethod
    def from_args(cls, args):
        """Instantiate a PuzzleRun from command line arguments"""
        if len(args) < 2:
            raise SetupError("Missing day number")
        day = _parse_day(args[1])
        other_digit = [a for a in args[2:] if a.isdigit()]
        if len(other_digit) > 1:
            raise SetupError("Too many numerical arguments")
        if other_digit:
            part = _parse_part(other_digit[0])
            parts = (part,)
        else:
            parts = (1, 2)
        skip_tests = "-s" in args[2:]
        return Puzzle(day, parts, skip_tests)

    def _instantiate_solver(self):
        try:
            solver_cls = getattr(
                import_module(f"{SOLVERS}.day{self.day}"),
                f"Day{self.day}Solver"
            )
            self.solver = solver_cls()
        except ModuleNotFoundError:
            raise SetupError(f"No solver code for Day {self.day}")

    def _parsed_input(self, filename):
        try:
            with open(filename) as input:
                return self.solver.parse(input)
        except FileNotFoundError:
            raise SetupError(f"Missing expected file {filename}")

    def _parse_test(self, filename):
        try:
            with open(filename) as input:
                header = input.readline().strip()
                if header[0] != EXPECTED_MARKER:
                    raise SetupError(
                        f"File {filename} missing expected solution value")
                parsed_input = self.solver.parse(input)
                return parsed_input, header[1:]
        except FileNotFoundError:
            raise SetupError(f"Missing expected file {filename}")

    def _collect_inputs(self):
        self.inputs["main"] = self._parsed_input(f"{INPUTS}/day{self.day}")
        self.inputs["tests"] = {1: {}, 2: {}}
        test_stem = f"{INPUTS}/day{self.day}-test"
        files = glob(f"{test_stem}*")
        for file in files:
            id = file[len(test_stem):]  # part number and (optional) label
            part = _parse_part(id[0])
            label = id[1:]
            self.inputs["tests"][part][label] = self._parse_test(file)

    def _solve_and_report(self, part, label, puzzle_input, expected=None):
        result = self.solver.solve(part, *puzzle_input)
        if expected:
            if str(result) == expected:
                msg = "pass"
            else:
                msg = "FAILED - expected {expected}, got {result}"
        else:
            msg = result
        print(f"  {label}: {msg}")

    def solve(self):
        print(f"==== Day {self.day} ====")
        print()
        for part in self.parts:
            print(f"Part {part}")
            if not self.skip_tests:
                for label, test_data in self.inputs["tests"][part].items():
                    test_input, expected = test_data
                    self._solve_and_report(part, f"Test{label.capitalize()}",
                                           test_input, expected)
            self._solve_and_report(part, "Solution", self.inputs["main"])
            print()


def _parse_int(x, label, lower, upper):
    try:
        n = int(x)
    except ValueError:
        raise SetupError(f"Invalid {label} number '{x}'")
    if n < lower or n > upper:
        raise SetupError(
            f"Invalid {label} number {n}, must be {lower}-{upper}")
    return n


def _parse_day(x):
    return _parse_int(x, "day", 1, 25)


def _parse_part(x):
    return _parse_int(x, "part", 1, 2)


def main():
    try:
        puzzle = Puzzle.from_args(argv)
        puzzle.solve()
    except SetupError as e:
        print()
        print(f"*** Setup failed: {e}.")


if __name__ == '__main__':
    main()