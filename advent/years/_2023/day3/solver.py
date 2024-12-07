import re

from advent.solver_base import Solver


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

    def _row_window(self, row):
        return range(max(0, row - 1), min(row + 2, self.num_rows))
    
    def _in_col_window(self, col, startcol, endcol):
        return col >= startcol - 1 and col <= endcol + 1

class Part1(Day3):
    def _check_adjacent(self, row, span):
        return any(
            self._in_col_window(symbol_col, *span)
            for r in self._row_window(row)
            for _, symbol_col in self.symbols[r]
        )

    def solve(self):
        return sum(
            entry[0]
            for r, entries in enumerate(self.numbers)
            for entry in entries
            if self._check_adjacent(r, entry[1:])
        )
    

class Part2(Day3):
    def _adjacent_nums(self, row, symbol_col):
        return tuple(
            num
            for r in self._row_window(row)
            for num, *span in self.numbers[r]
            if self._in_col_window(symbol_col, *span)
        )
    
    def solve(self):
        return sum(
            nums[0] * nums[1]
            for r, symbol_entries in enumerate(self.symbols)
            for symbol, symbol_col in symbol_entries
            if symbol == "*" and
            len(nums := self._adjacent_nums(r, symbol_col)) == 2
        )
