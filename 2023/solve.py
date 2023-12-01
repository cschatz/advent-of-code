from importlib import import_module
from sys import argv

INPUTS = "inputs"
TESTS = "tests"

def parse_args(args):
    if len(args) < 2:
        raise Exception("Missing day number")
    if len(args) > 3:
        raise Exception("Too many arguments")
    day = args[1]
    test = args[2] if len(args) == 3 else ""
    return day, test


def main():
    try:
        day, test = parse_args(argv)
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
            solution = solver.solve(*parsed_input)
            if type(solution) == str:
                solution = "\n" + solution
            print(f"Solution: {solution}")

    except Exception as e:
        print(f"*** ERROR: {e}")


if __name__ == '__main__':
    main()
