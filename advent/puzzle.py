from .util import (
    collect_inputs,
    instantiate_solver,
    SetupError,
)


class Puzzle:
    """Represent applying solver code to a particular day's puzzle,
    optionally including test input in addition to the main puzzle input."""

    def __init__(self, year, day, parts, include_tests, include_puzzle):
        self.day = day
        self.parts = parts
        self.include_tests = include_tests
        self.include_puzzle = include_puzzle
        solver = instantiate_solver(year, day)
        self.inputs = collect_inputs(year, day, solver)
        self.solver = solver

    def _solve_one(self, part, input, expected=None):
        result = self.solver.solve(part, *input)
        if expected:
            if str(result) == expected:
                return "pass"
            else:
                return f"FAILED - expected {expected}, got {result}"
        else:
            return result

    def solve(self):
        print(f"==== Day {self.day} ====")
        print()
        for part in self.parts:
            print(f"Part {part}")
            if self.include_tests:
                for label, input_data in self.inputs[part].items():
                    label = " {label.capitalize()}" if label else ""
                    result = self._solve_one(
                        part, input_data["input"], expected=input_data["expected"])
                    print(f"  Test{label}: {result}")
            if self.include_puzzle:
                result = self._solve_one(part, self.inputs["primary"])
                print(f"  Solution: {result}")
            print()
        # print()
        # for part in self.parts:
        #     print(f"Part {part}")
        #     if not self.skip_tests:
        #         for label, test_data in self.inputs["tests"][part].items():
        #             test_input, expected = test_data
        #             self._solve_and_report(part, f"Test{label.capitalize()}",
        #                                    test_input, expected)
        #     if not self.skip_main:
        #         self._solve_and_report(part, "Solution", self.inputs["main"])
        #     print()
