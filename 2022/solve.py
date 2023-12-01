from importlib import import_module
from sys import argv


def main():
    day = argv[1]
    if len(argv) == 3 and argv[2][:2] == "-t":
        test = f"-test{argv[2][2:]}"
    else:
        test = ""
    for part in (1, 2):
        with open(f"inputs/day{day}{test}.txt") as input:
            parse = getattr(
                import_module(f"solvers.day{day}"),
                f"day{day}_parse"
            )
            solve = getattr(
                import_module(f"solvers.day{day}"),
                f"day{day}_{part}"
            )
            solution = solve(*parse(input))
            if type(solution) == str:
                solution = "\n" + solution
            print(f"Part {part}:", solution)


if __name__ == '__main__':
    main()
