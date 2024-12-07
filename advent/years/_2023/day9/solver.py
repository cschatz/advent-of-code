from advent.solver_base import Solver


class Day9(Solver):
    def parse(self, lines):
        self.histories = [
            tuple(int(x) for x in line.split(" "))
            for line in lines
        ]

class Part1(Day9):
    def solve(self):
        return sum(_next_value(h) for h in self.histories)


class Part2(Day9):
    def solve(self):
        return sum(_next_value(tuple(reversed(h))) for h in self.histories)



def _next_value(seq):
    seqs = [seq]
    while True:
        next_seq, end = _diff_seq(seqs[-1])
        seqs.append(next_seq)
        if end:
            break
    return sum(seq[-1] for seq in seqs)





def _diff_seq(seq):
    out = []
    all_zeros = True
    for i in range(1, len(seq)):
        delta = seq[i] - seq[i - 1]
        if delta != 0:
            all_zeros = False
        out.append(delta)
    return out, all_zeros    
