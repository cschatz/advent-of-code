from glob import glob
from importlib import import_module

DAY_PATH = "advent/puzzles_{}/day{}/"
INPUT_PATH = DAY_PATH + "inputs/"
PUZZLE_PATH = INPUT_PATH + "puzzle" 
TEST_PATH = INPUT_PATH + "test{}"


class PuzzleError(Exception):
    ...


class Puzzle:
    """Encapsulates applying solver code to particular day(s) inputs,
    optionally including test inputs in addition to the main puzzle input."""

    def __init__(self, year, day, parts, include_puzzle, include_tests):
        self.parts = parts
        self.include_puzzle = include_puzzle
        self.include_tests = include_tests
        self.puzzle_solvers = []
        self.test_solvers = []
        if include_puzzle:
            puzzle_input, _ = _input_from_file(PUZZLE_PATH.format(year, day))
            for part in parts:
                self.puzzle_solvers.append(_solver_class(year, day, part)(puzzle_input))
        if include_tests:
            for part in parts:
                files = glob(f"{TEST_PATH}*".format(year, day, part))
                if not files:
                    raise PuzzleError(f"Missing expected test input(s) for day {day} part {part}")
                part_test_solvers = []
                for filename in files:
                    test_input, expected = _input_from_file(filename, is_test=True)
                    name = filename[len(TEST_PATH):].capitalize()
                    label = "Test" + (f" {name}" if name else "")
                    solver = _solver_class(year, day, part)(test_input)
                    part_test_solvers.append((label, solver, expected))
                self.test_solvers.append(part_test_solvers)

    def solve(self):
        for i, part in enumerate(self.parts):
            print(f"\n  --- Part {part} ---")
            if self.test_solvers:
                for label, test_solver, expected in self.test_solvers[i]:
                    test_result = test_solver.solve()
                    print(f"  {label}: {_test_msg(test_result, expected)}")
            if self.puzzle_solvers:
                result = self.puzzle_solvers[i].solve()
                print(f"  Solution: {result}")


def _open_file(filename):
    try:
        file = open(filename)
        return file
    except FileNotFoundError:
        raise PuzzleError(f"Missing expected file '{filename}'")


def _input_from_file(filename, is_test=False):
    with _open_file(filename) as file:
        expected = None
        if is_test:
            header = file.readline().strip()
            if header[:10] != "#expected:":
                raise PuzzleError(f"Missing expected solution in {filename}")
            expected = header[10:]
        lines = [line.strip() for line in file.readlines()]
        return lines, expected


def _solver_class(year, day, part):
    module_path = f"advent.puzzles_{year}.day{day}.solver"
    solver_cls_name = f"Part{part}"
    try:
        solver_cls = getattr(
            import_module(module_path),
            solver_cls_name
        )
        return solver_cls
    except (ModuleNotFoundError, AttributeError):
        raise PuzzleError(f"Missing solver code for day {day} part {part}")

def _test_msg(actual, expected):
    if str(actual) == str(expected):
        return "pass"
    else:
        return f"FAIL: {actual} (expected {expected})"