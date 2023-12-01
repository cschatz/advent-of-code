import re

from util import input_lines


def day5_parse(file):
    stacks = [[] for _ in range(9)]
    moves = []
    lines = input_lines(file)
    line_num = 0
    for line in lines:
        if "[" in line:
            crate_data = ((i//4, line[i+1]) for i in range(0, len(line), 4) if line[i+1] != " ")
            for stack, crate in crate_data:
                stacks[stack].insert(0, crate)
            line_num += 1
        else:
            pass
    for line in lines[line_num+2:]:
        moves.append(re.findall(r'\d+', line))
    return stacks, moves


def move_crates(stacks, count, src, dst, flip=True):
    moving = stacks[src-1][-count:]
    stacks[src-1][-count:] = []
    if flip:
        moving = moving[::-1]
    stacks[dst-1].extend(moving)


def day5_1(stacks, moves):
    for move in moves:
        move_crates(stacks, *[int(x) for x in move])
    return "".join(stack[-1] for stack in stacks)


def day5_2(stacks, moves):
    for move in moves:
        move_crates(stacks, *[int(x) for x in move], flip=False)
    return "".join(stack[-1] for stack in stacks)
