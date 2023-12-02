import re
from collections import defaultdict
from glob import glob
from importlib import import_module
from os import path


class SetupError(Exception):
    pass


def parse_args(args):
    if len(args) < 3:
        raise SetupError("Year and day required")
    year = _validate_year(args[1])
    day = _validate_day(args[2])
    other_digit = [a for a in args[3:] if a.isdigit()]
    if len(other_digit) > 1:
        raise SetupError("Too many numerical arguments")
    if other_digit:
        part = _validate_part(other_digit[0])
        parts = (part,)
    else:
        parts = ("1", "2")
    include_tests = "-p" not in args[3:]  # puzzle only
    include_puzzle = "-t" not in args[3:]  # tests only
    return (year, day, parts, include_tests, include_puzzle)


def instantiate_solver(year, day):
    module_path = f"advent.puzzles_{year}.solvers.day{day}"
    solver_cls_name = f"Day{day}Solver"
    try:
        solver_cls = getattr(
            import_module(module_path),
            solver_cls_name
        )
        return solver_cls()
    except ModuleNotFoundError:
        raise SetupError(f"Missing solver code for day {day}")


def collect_inputs(year, day, solver):
    inputs = defaultdict(dict)
    files = glob(f"advent/puzzles_{year}/inputs/*")
    for file in files:
        name = path.basename(file)
        m = re.match(r'^day(\d+)(?:-test(\d)(.+)?)?$', name)
        if not m:
            raise SetupError(f"Invalid input filename: {file}")
        input_day, part, label = m.groups()
        if input_day == day:
            input_data = _parse_input(file, solver, is_test=part is not None)
            if part is None:
                inputs["primary"] = input_data["input"]
            else:
                inputs[part][label] = input_data
    return inputs


def _parse_input(filename, solver, is_test=False):
    with _open_file(filename) as input:
        if is_test:
            header = input.readline().strip()
            if header[:10] != "#expected:":
                raise SetupError(f"Missing expected solution in {filename}")
        parsed_input = solver.parse(input)
        out = dict(input=parsed_input)
        if is_test:
            out.update(dict(expected=header[10:]))
        return out


def _open_file(filename):
    try:
        f = open(filename)
        return f
    except FileNotFoundError:
        raise SetupError(f"Missing file '{filename}")


def _validate_int(x, label, lower, upper):
    try:
        n = int(x)
    except ValueError:
        raise SetupError(f"Invalid {label} number '{x}'")
    if n < lower or n > upper:
        raise SetupError(
            f"Invalid {label} number {n}, must be {lower}-{upper}")
    return x


def _validate_day(x):
    return _validate_int(x, "day", 1, 25)


def _validate_part(x):
    return _validate_int(x, "part", 1, 2)


def _validate_year(x):
    return _validate_int(x, "year", 2020, 9999)
