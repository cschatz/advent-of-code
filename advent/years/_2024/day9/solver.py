from dataclasses import dataclass
from bisect import bisect_left

from advent.solver_base import Solver

def file_at_block(file_id, block_pos):
    return file_id * block_pos

class Part1(Solver):
    def parse(self, lines):
        self.disk_map = list(int(x) for x in lines[0])

    def __init__(self, lines):
        super().__init__(lines)
        map_len = len(self.disk_map)
        self.left_map_idx = 0
        self.left_file_id = 0
        self.left_block_pos = 0
        self.right_map_idx = map_len - 1
        self.right_file_id = map_len // 2
        self.checksum = 0

    def check_or_update_left(self):
        # update left, return True if in free area
        left_is_free = self.left_map_idx % 2 == 1
        if left_is_free:
            if self.disk_map[self.left_map_idx] > 0:
                return True
            else:
                self.left_map_idx += 1
                return False
        else:
            if self.disk_map[self.left_map_idx] == 0:
                self.left_map_idx += 1
                self.left_file_id += 1
            else:
                self.checksum += file_at_block(self.left_file_id, self.left_block_pos)
                self.disk_map[self.left_map_idx] -= 1
                self.left_block_pos += 1
            return False
            
    def check_or_update_right(self):
        right_is_free = self.right_map_idx % 2 == 1
        if right_is_free:
            self.right_map_idx -= 1
        else:
            if self.disk_map[self.right_map_idx] == 0:
                self.right_map_idx -= 1
                self.right_file_id -= 1
            else:
                self.checksum += file_at_block(self.right_file_id, self.left_block_pos)
                self.disk_map[self.left_map_idx] -= 1
                self.disk_map[self.right_map_idx] -= 1
                self.left_block_pos += 1

    def solve(self):
        while self.left_map_idx <= self.right_map_idx:
            left_at_free = self.check_or_update_left()
            if left_at_free:
                self.check_or_update_right()

        return self.checksum


@dataclass
class File:
    id: int
    pos: int
    length: int

@dataclass
class Free:
    pos: int
    length: int

class Part2(Part1):
    def solve(self):

        block_pos = 0
        file_id = 0
        files = []
        frees = []
        is_file = True
        for length in self.disk_map:
            if is_file:
                files.insert(0, File(file_id, block_pos, length))
                file_id += 1
            else:
                 frees.append(Free(block_pos, length))
            block_pos += length
            is_file = not is_file

        checksum = 0
        for file in files:
            file_len = file.length
            try:
                free = next(
                    filter(
                        lambda f: f.pos < file.pos and f.length >= file.length,
                        frees
                    )
                )
                file_pos = free.pos
                free.length -= file_len
                free.pos += file_len
            except StopIteration:
                file_pos = file.pos
            checksum += sum(file.id * (file_pos + i) for i in range(file_len))
        return checksum
