from advent.solver_base import Solver

def file_at_block(file_id, block_pos):
    # print(f"File {file_id} at block {block_pos}")
    return file_id * block_pos

class Part1(Solver):
    def parse(self, lines):
        self.disk_map = list(int(x) for x in lines[0])

    def __init__(self, lines):
        super().__init__(lines)
        map_len = len(self.disk_map)
        assert map_len % 2 == 1
        
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

class Part2(Part1):
    ...



"""

[2, 3, 3, 3, 1, 3, 3, 1, 2, 1, 4, 1, 4, 1, 3, 1, 4, 0, 2]



"""