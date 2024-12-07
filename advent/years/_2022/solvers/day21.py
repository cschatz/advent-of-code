from advent.util import input_lines

def day21_parse(file):
    data = {}
    for line in input_lines(file):
        monkey, expr = line[:4], line[6:]
        if expr.isdigit():
            data[monkey] = int(expr)
        else:
            data[monkey] = expr.split(" ")
    return (data,)


def day21_1(data):
    def calc(expr):
        if type(expr) == int:
            return expr
        else:
            left, right = map(calc, (data[expr[0]], data[expr[2]]))
            op = expr[1]
            return eval(f"{left} {op} {right}")
    return int(calc(data["root"]))

def day21_2(data):
    data["humn"] = "x"
    data["root"][1] = "=="
    def parse(expr):
        if type(expr) == int or expr == "x":
            return expr
        else:
            left, right = map(parse, (data[expr[0]], data[expr[2]]))
            op = expr[1]
            parsed = f"{left} {op} {right}"
            if op != "==" and "x" not in parsed:
                return eval(parsed)
            else:
                return f"({parsed})"
    return parse(data["root"])