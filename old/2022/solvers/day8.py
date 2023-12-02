from collections import defaultdict

from advent.util import input_lines


def day8_parse(file):
    lines = input_lines(file)
    grid = [[int(c) for c in line] for line in lines]
    return grid


def check_seq(heights, seq, vis):
    # check visibility of a sequence,
    # iterating one direction
    tallest = -1
    for h, p in zip(heights, seq):
        if h > tallest:
            tallest = h
            vis.add(p)


def check_span(treemap, seq, vis):
    # check visibility of a sequence,
    # combining both directions
    heights = [treemap[r][c] for r, c in seq]
    check_seq(heights, seq, vis)
    check_seq(heights[::-1], seq[::-1], vis)


def day8_1(*treemap):
    vis = set()
    nr = len(treemap)
    nc = len(treemap[0])
    for r in range(nr):
        seq = [(r, c) for c in range(nc)]
        check_span(treemap, seq, vis)
    for c in range(nc):
        seq = [(r, c) for r in range(nr)]
        check_span(treemap, seq, vis)
    return len(vis)


def score_seq(heights, seq, scores):
    # when was something blocking each height 0-9 seen?
    last_blocker = [0] * 10
    for i, h, p in zip(range(len(heights)), heights, seq):
        score = i - last_blocker[h]
        for k in range(h+1):
            last_blocker[k] = i
        scores[p] *= score


def score_span(treemap, seq, scores):
    heights = [treemap[r][c] for r, c in seq]
    score_seq(heights, seq, scores)
    score_seq(heights[::-1], seq[::-1], scores)


def day8_2(*treemap):
    scores = defaultdict(lambda: 1)  # view scores per position
    nr = len(treemap)
    nc = len(treemap[0])
    for r in range(nr):
        seq = [(r, c) for c in range(nc)]
        score_span(treemap, seq, scores)
    for c in range(nc):
        seq = [(r, c) for r in range(nr)]
        score_span(treemap, seq, scores)
    return max(scores.values())
