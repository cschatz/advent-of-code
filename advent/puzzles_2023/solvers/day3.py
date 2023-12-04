import re

from .base import Solver


class Day3(Solver):

    def parse(self, lines):
        self.numbers = []
        self.symbols = []
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
            self.numbers.append(number_row)
            self.symbols.append(symbol_row)
        self.num_rows = len(self.numbers)

    def _adj_row_range(self, row):
        return range(max(0, row - 1), min(row + 2, self.num_rows))

class Day3Part1(Day3):
    def _check_adjacent(self, row, number_entry):
        startcol, endcol = number_entry[1:]
        return any(
            symbol_col in range(startcol - 1, endcol + 2)
            for r in self._adj_row_range(row)
            for _, symbol_col in self.symbols[r]
        )

    def solve(self):
        return sum(
            entry[0]
            for r, entries in enumerate(self.numbers)
            for entry in entries
            if self._check_adjacent(r, entry)
        )
    

class Day3Part2(Day3):
    def adj_nums(self, row, symbol_col):
        return tuple(
            n
            for r in self._adj_row_range(row)
            for n, startcol, endcol in self.numbers[r]
            if symbol_col in range(startcol - 1, endcol + 2)
        )
    
    def solve(self):
        return sum(
            nn[0] * nn[1]
            for nn in (
                self.adj_nums(r, symbol_col)
                for r, symbol_entries in enumerate(self.symbols)
                for symbol, symbol_col in symbol_entries
                if symbol == "*"
            )
            if len(nn) == 2
        )
