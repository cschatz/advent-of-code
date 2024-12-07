from importlib import import_module

from .error import PuzzleError


def _open_file(filename):
    try:
        return open(filename)
    except FileNotFoundError:
        raise PuzzleError(f"Missing expected file '{filename}'")


def input_from_file(filename, is_test=False):
    with _open_file(filename) as file:
        expected = None
        if is_test:
            header = file.readline().strip()
            if header[:10] != "#expected:":
                raise PuzzleError(f"Missing expected solution in {filename}")
            expected = header[10:]
        lines = [line.strip() for line in file.readlines()]
        return lines, expected


def solver_class(year, day, part):
    try:
        return getattr(
            import_module(f"advent.puzzles_{year}.day{day}.solver"),
            f"Part{part}"
        )
    except (ModuleNotFoundError, AttributeError):
        raise PuzzleError(f"Missing solver code for day {day} part {part}")


def _validate_int(x, label, lower, upper):
    try:
        n = int(x)
    except ValueError:
        raise PuzzleError(f"Invalid {label} number '{x}'")
    if n < lower or n > upper:
        raise PuzzleError(
            f"Invalid {label} number {n}, must be {lower}-{upper}")
    return int(x)


def _validate_day(x):
    return _validate_int(x, "day", 1, 25)


def validate_day_range(x):
    if "-" not in x:
        return (_validate_day(x),)
    else:
        begin_end = x.split("-")
        begin, end = (_validate_day(d) for d in begin_end)
        if end < begin:
            raise PuzzleError("Invalid day range")
        return range(begin, end + 1)


def validate_part(x):
    return _validate_int(x, "part", 1, 2)


def validate_year(x):
    return _validate_int(x, "year", 2020, 9999)


