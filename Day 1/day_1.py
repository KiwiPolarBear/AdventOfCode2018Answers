import os
from typing import List


def parse_input() -> List[str]:
    """ Reads the input file and returns a list of strings. """
    file_location = os.path.join(os.path.dirname(__file__), 'input.txt')
    input_values = []
    with open(file_location, 'r') as data:
        for line in data:
            input_values.append(line.strip())
    return input_values


def input_gen(input_data: List[str]):
    """ A generator that will continuously iterate over the given list. """
    while True:
        for item in input_data:
            yield item


# ============================ Part One ===============================


def part_one(input_data: List[str]):
    """ Puzzle Answer == 400 """
    total = 0
    for item in input_data:
        total += int(item)
    print(total)


# ============================ Part Two ===============================


def part_two(input_data: List[str]):
    """ Puzzle Answer == 232 """
    total = 0
    already_seen = [0]
    for item in input_gen(input_data):
        total += int(item)
        if total not in already_seen:
            already_seen.append(total)
        else:
            break
    print(total)


# =====================================================================


if __name__ == '__main__':
    input_list = parse_input()
    part_one(input_list)
    part_two(input_list)
