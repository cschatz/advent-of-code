from advent.util import input_lines


def day2_parse(file):
    return [line.split(" ") for line in input_lines(file)]


def score(opp, me):
    opp = "ABC".index(opp) + 1
    me = "XYZ".index(me) + 1
    diff = me - opp
    outcome = 3 if diff == 0 else (6 if diff in (1, -2) else 0)
    return me + outcome


def score_with_outcome(opp, outcome):
    opp = "ABC".index(opp)
    if outcome == "X":  # need to lose
        outcome_score = 0
        me = (opp + 2) % 3
    elif outcome == "Z":  # need to win
        outcome_score = 6
        me = (opp + 1) % 3
    else:
        outcome_score = 3
        me = opp
    return me + 1 + outcome_score


def day2_1(*plays):
    return sum(score(*play) for play in plays)


def day2_2(*plays):
    return sum(score_with_outcome(*play) for play in plays)
