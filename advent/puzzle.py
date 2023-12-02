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
                test_inputs = self.inputs.get(part)
                if not test_inputs:
                    raise SetupError(f"No tests provided for part {part}")
                for label, input_data in test_inputs.items():
                    label = " {label.capitalize()}" if label else ""
                    result = self._solve_one(
                        part,
                        input_data["input"],
                        expected=input_data["expected"]
                    )
                    print(f"  Test{label}: {result}")
            if self.include_puzzle:
                primary_input = self.inputs.get("primary")
                if not primary_input:
                    raise SetupError("No puzzle input provided")
                result = self._solve_one(part, self.inputs["primary"])
                print(f"  Solution: {result}")
            print()
