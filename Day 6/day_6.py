import math
import os
from collections import defaultdict
from typing import List, Tuple, Optional


def parse_input() -> List[str]:
    """ Reads the input file and returns a list of strings. """
    file_location = os.path.join(os.path.dirname(__file__), 'input.txt')
    input_values = []
    with open(file_location, 'r') as data:
        for line in data:
            input_values.append(line.strip())
    return input_values


def manhattan_distance(point_a: Tuple[int, int], point_b: Tuple[int, int]) -> int:
    """ Returns the manhattan distance between the two points. """
    return abs(point_a[0] - point_b[0]) + abs(point_a[1] - point_b[1])


def find_closest(grid_coordinate: Tuple[int, int], node_list: List[Tuple[int, int]]) -> Optional[Tuple[int, int]]:
    """
    Returns the node that is closest to the given point.
    Returns None if two nodes are the same distance.
    """
    closest_node = None
    shortest_distance = math.inf
    for node in node_list:
        distance = manhattan_distance(node, grid_coordinate)
        if distance < shortest_distance:
            closest_node = node
            shortest_distance = distance
        elif distance == shortest_distance:
            closest_node = None
    return closest_node


def get_manhattan_sum(grid_coordinate: Tuple[int, int], node_list: List[Tuple[int, int]]) -> int:
    """
    Returns the sum of the manhattan distances from the given co-ordinate,
    to all the node co-ordinates in the given list.
    """
    distances = [manhattan_distance(grid_coordinate, x) for x in node_list]
    return sum(distances)


# ============================ Part One ===============================


def part_one(input_data: List[str]):
    """ Puzzle Answer == 3722 """
    coordinates = list(map(lambda item: (int(item.split(',')[0]), int(item.split(',')[1])), input_data))
    max_x = max(coordinates, key=lambda x: x[0])[0]
    max_y = max(coordinates, key=lambda x: x[1])[1]
    grid_dict = defaultdict(lambda: [])

    # Generate the grid dictionary.
    for x in range(max_x):
        for y in range(max_y):
            closest_node = find_closest((x, y), coordinates)
            if closest_node:
                grid_dict[closest_node].append((x, y))

    # Remove infinite areas from dictionary.
    for node_tup, grid_list in grid_dict.items():
        for x, y in grid_list:
            if x in (0, max_x) or y in (0, max_y):
                grid_dict[node_tup] = []
                break

    # Find the largest area.
    highest_area = 0
    for key, val in grid_dict.items():
        if len(val) > highest_area:
            highest_area = len(val)

    print(highest_area)


# ============================ Part Two ===============================


def part_two(input_data: List[str]):
    """ Puzzle Answer == 44634 """
    coordinates = list(map(lambda item: (int(item.split(',')[0]), int(item.split(',')[1])), input_data))
    max_x = max(coordinates, key=lambda x: x[0])[0]
    max_y = max(coordinates, key=lambda x: x[1])[1]
    total_area = 0

    for x in range(max_x):
        for y in range(max_y):
            if get_manhattan_sum((x, y), coordinates) < 10000:
                total_area += 1

    print(total_area)


# =====================================================================


if __name__ == '__main__':
    input_list = parse_input()
    part_one(input_list)
    part_two(input_list)
