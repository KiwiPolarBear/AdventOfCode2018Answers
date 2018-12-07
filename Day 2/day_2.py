import os
from typing import List, Optional, Tuple


def parse_input() -> List[str]:
    """ Reads the input file and returns a list of strings. """
    file_location = os.path.join(os.path.dirname(__file__), 'input.txt')
    input_values = []
    with open(file_location, 'r') as data:
        for line in data:
            input_values.append(line.strip())
    return input_values


def is_2_or_3(input_string: str) -> Tuple[bool, bool]:
    """
    Returns a tuple of booleans indicating whether a string contains any
    character exactly 2 or 3 times.
    """
    alpha = 'abcdefghijklmnopqrstuvwxyz'
    seen_dict = {char: 0 for char in alpha}

    for letter in input_string:
        seen_dict[letter] += 1

    counts = set(seen_dict.values())
    return 2 in counts, 3 in counts


def find_common_ids(id_string: str, id_list: List[str]) -> Optional[str]:
    """
    Iterates through the given list, to find a match to the given string,
    where the two strings are identical except for a single character at
    the same index.

    Returns None if there is no matching string in the given list.
    """
    match = None
    for item in id_list:
        diffs = 0
        for index, char in enumerate(item):
            if char != id_string[index]:
                diffs += 1
        if diffs == 1:
            match = item
            break
    return match


# ============================ Part One ===============================


def part_one(input_data: List[str]):
    """ Puzzle Answer == 8296 """
    twos = 0
    threes = 0

    for string_val in input_data:
        is_two, is_three = is_2_or_3(string_val)

        twos += 1 if is_two else 0
        threes += 1 if is_three else 0

    check_sum = twos * threes
    print(check_sum)


# ============================ Part Two ===============================


def part_two(input_data: List[str]):
    """ Puzzle Answer == pazvmqbftrbeosiecxlghkwud """
    for index, item in enumerate(input_data):
        match = find_common_ids(item, input_data[index+1:])
        if match:
            print(''.join([i for i in list(item) if i in list(match)]))


# =====================================================================


if __name__ == '__main__':
    input_list = parse_input()
    part_one(input_list)
    part_two(input_list)
