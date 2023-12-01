def input_all(file, drop_final_newline=True):
    all = file.read()
    if drop_final_newline:
        all = all.rstrip()
    return all


def input_lines(file, lstrip=False, rstrip=True):
    def prep(line):
        if lstrip:
            line = line.lstrip()
        if rstrip:
            line = line.rstrip()
        return line
    return [prep(line) for line in file.readlines()]
