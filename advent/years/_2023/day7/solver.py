from advent.solver_base import Solver

from collections import Counter


class Day7(Solver):
    FACES = {}

    def parse(self, lines):
        self.hands = []
        for line in lines:
            cards, bid = line.split(" ")
            faces = tuple(self.FACES[c] for c in cards)
            group_counts = self._group_counts(faces)
            key = (self._tier(group_counts), *faces)
            self.hands.append((key, int(bid), cards))

    def _count_map(self, faces):
        return Counter(faces)

    def _group_counts(self, faces):
        count_map = self._count_map(faces)
        return sorted(count_map.values(), reverse=True)

    def _tier(self, counts):
        if all(c == 1 for c in counts):  # high card only
            return 0
        elif counts[0] == 2:  # one pair or two pair
            if len(counts) > 1 and counts[1] == 2:
                return 2
            else:
                return 1
        elif counts[0] == 3:  # 3 of a hind or full house
            if len(counts) > 1 and counts[1] == 2:
                return 4
            else:
                return 3
        else:
            # 4 or 5 of a kind -> tier 5 or 6
            return counts[0] + 1

    def solve(self):
        self.hands.sort(key=lambda h: h[0])
        return sum(
            rank * hand[1] for rank, hand in enumerate(self.hands, 1)
        )


class Part1(Day7):
    FACES = dict(zip("23456789TJQKA", range(13)))


class Part2(Day7):
    FACES = dict(zip("J23456789TQKA", range(13)))

    def _group_counts(self, faces):
        count_map = self._count_map(faces)
        jacks = count_map.pop(0) if 0 in count_map else 0
        group_counts = sorted(count_map.values(), reverse=True)
        if len(group_counts) > 0:
            group_counts[0] += jacks
        else:
            group_counts.append(5)
        return group_counts
