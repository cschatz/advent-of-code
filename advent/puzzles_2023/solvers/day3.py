import re

from .base import Solver


class Day3Solver(Solver):

    def parse(self, file):
        numbers = []
        symbols = []
        lines = super().parse(file)
        for line in lines:
            number_row = []
            symbol_row = []
            chunks = re.findall(r'(\d+|\.+|[^\.\d])', line)
            col = 0
            for chunk in chunks:
                clen = len(chunk)
                if chunk.isdigit():
                    number_row.append((int(chunk), col, col + clen - 1))
                elif chunk[0] != ".":
                    symbol_row.append((chunk, col))
                col += clen
            numbers.append(number_row)
            symbols.append(symbol_row)
        return numbers, symbols

    def solve_part1(self, numbers, symbols):

        num_rows = len(numbers)

        def check_adj(row, number_entry):
            startcol, endcol = number_entry[1:]
            for rr in range(max(0, row - 1), min(row + 2, num_rows)):
                for _, symbol_col in symbols[rr]:
                    if symbol_col in range(startcol - 1, endcol + 2):
                        return True

        sum = 0
        for r, entries in enumerate(numbers):
            for entry in entries:
                if check_adj(r, entry):
                    sum += entry[0]
        return sum

    def solve_part2(self, numbers, symbols):

        num_rows = len(numbers)

        def gear_ratio(row, symbol_col):
            adj_numbers = []
            for rr in range(max(0, row - 1), min(row + 2, num_rows)):
                for n, startcol, endcol in numbers[rr]:
                    if symbol_col in range(startcol - 1, endcol + 2):
                        adj_numbers.append(n)
            if len(adj_numbers) == 2:
                return adj_numbers[0] * adj_numbers[1]
            else:
                return 0

        sum = 0
        for r, symbol_entries in enumerate(symbols):
            for symbol, symbol_col in symbol_entries:
                if symbol == "*":
                    sum += gear_ratio(r, symbol_col)
        return sum
