from util import input_all


def day6_parse(file):
    return input_all(file)


def chars_needed(signal, window_size):
    for i in range(len(signal) - window_size):
        s = set(signal[i:i+window_size])
        if len(s) == window_size:
            return i + window_size


def day6_1(*data):
    return chars_needed(data, 4)


def day6_2(*data):
    return chars_needed(data, 14)
