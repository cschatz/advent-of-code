from bisect import bisect_right
from advent.util import input_lines


def day10_parse(file):
    return [
        int(line[5:]) if len(line) > 5 else None for line in input_lines(file)
    ]


def day10_values(*program):
    x = 1
    cycle = 0
    values = [(0, x)]
    for n in program:
        if not n:
            cycle += 1
        else:
            cycle += 2
            x += n
            values.append((cycle, x))
    return values


def day10_1(*program):
    values = day10_values(*program)
    check_cycles = [19] + list(range(59, 221, 40))

    def x(cycle):
        i = bisect_right(values, cycle, key=lambda n: n[0]) - 1
        return values[i][1]

    return sum((cycle + 1) * x(cycle) for cycle in check_cycles)


def day10_2(*program, w=40, h=6):
    values = day10_values(*program)

    def sprite_gen():
        for current, next in (values[i:i+2] for i in range(len(values)-1)):
            for _ in range(next[0] - current[0]):
                yield current[1]
        while True:
            yield values[-1][1]

    def pixel(x, i):
        return "#" if abs(x - i % w) <= 1 else "."

    def render(pixels):
        return "\n".join("".join(pixels[r * w:(r + 1) * w]) for r in range(h))

    display = render(list(map(pixel, sprite_gen(), range(w * h))))
    return(display)
