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


def collapse_string(input_str: str) -> str:
    """ Collapses a polymer string. """
    index = 0
    while index + 1 != len(input_str):
        char1, char2 = input_str[index], input_str[index + 1]
        if char1.lower() == char2.lower():
            if sum([char1.islower(), char2.islower()]) == 1:
                input_str = input_str[:index] + input_str[index + 2:]
                index -= 2
        index += 1
    return input_str


# ============================ Part One ===============================


def part_one(input_data: List[str]):
    """ Puzzle Answer == 11754 """
    collapsed_string = collapse_string(input_data[0])
    print(len(collapsed_string))


# ============================ Part Two ===============================


def part_two(input_data: List[str]):
    """ Puzzle Answer == 4098 """
    lengths = []
    alpha = 'abcdefghijklmnopqrstuvwxyz'
    for char in alpha:
        input_str = ''.join(a for a in input_data[0] if a.lower() != char)
        collapsed_string = collapse_string(input_str)
        lengths.append(len(collapsed_string))
    print(min(lengths))


# =====================================================================


if __name__ == '__main__':
    input_list = parse_input()
    part_one(input_list)
    part_two(input_list)