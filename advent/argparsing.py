from .puzzle import PuzzleError


def parse_args(args):
    if len(args) < 3:
        raise PuzzleError("Year and day required")
    year = _validate_year(args[1])
    days = _validate_day_range(args[2])
    other_digit = [a for a in args[3:] if a.isdigit()]
    if len(other_digit) > 1:
        raise PuzzleError("Too many numerical arguments")
    if other_digit:
        part = _validate_part(other_digit[0])
        parts = (part,)
    else:
        parts = (1, 2)
    include_tests = "-p" not in args[3:]  # puzzle only
    include_puzzle = "-t" not in args[3:]  # tests only
    return (year, days, parts, include_puzzle, include_tests)


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


def _validate_day_range(x):
    if "-" not in x:
        return (_validate_day(x),)
    else:
        begin_end = x.split("-")
        begin, end = (_validate_day(d) for d in begin_end)
        if end < begin:
            raise PuzzleError("Invalid day range")
        return range(begin, end + 1)

def _validate_part(x):
    return _validate_int(x, "part", 1, 2)


def _validate_year(x):
    return _validate_int(x, "year", 2020, 9999)


