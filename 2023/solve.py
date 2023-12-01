from importlib import import_module
from sys import argv

INPUTS = "inputs"
TESTS = "tests"

def parse_args(args):
    if len(args) < 2:
        raise Exception("Missing day number")
    if len(args) > 4:
        raise Exception("Too many arguments")
    day = args[1]
    part = args[2] if len(args) > 2 else "-"
    test = args[3] if len(args) == 4 else ""
    return day, part, test


def main():
    try:
        day, part, test = parse_args(argv)
        if test != "":
            input_filename = f"{TESTS}/day{day}-test{test}"
        else:
            input_filename = f"{INPUTS}/day{day}"
        with open(input_filename) as input:
            solver_cls = getattr(
                import_module(f"solvers.day{day}"),
                f"Day{day}Solver"
            )
            solver = solver_cls()
            parsed_input = solver.parse(input)
            parts = (1, 2) if part == "-" else (int(part),)
            for part in parts:
                solution = solver.solve(part, *parsed_input)
                if type(solution) == str:
                    solution = "\n" + solution
                print(f"Part {part} Solution: {solution}")

    except Exception as e:
        print(f"*** ERROR: {e}")


if __name__ == '__main__':
    main()
