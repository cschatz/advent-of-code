class TestFailure(Exception):
    pass


class Solver:

    def parse(self, file):
        return Solver.input_lines(file)

    @staticmethod
    def input_all(file, drop_final_newline=True):
        all = file.read()
        if drop_final_newline:
            all = all.rstrip()
        return all

    @staticmethod
    def input_lines(file, lstrip=False, rstrip=True):
        def prep(line):
            if lstrip:
                line = line.lstrip()
            if rstrip:
                line = line.rstrip()
            return line
        return [prep(line) for line in file.readlines()]

    def solve(self, part, *args):
        return (self.solve_part1(*args) if part == 1
                else self.solve_part2(*args))

    def solve_part1(self, *args):
        ...

    def solve_part2(self, *args):
        ...
