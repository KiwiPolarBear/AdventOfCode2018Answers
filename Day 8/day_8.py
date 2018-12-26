import os
from typing import List


class TreeNode:
    """ Represents a node in the tree. """

    number_of_children: int
    number_of_metadata: int
    child_nodes: List['TreeNode']
    metadata: List[int]

    def __init__(self):
        self.number_of_children = 0
        self.number_of_metadata = 0
        self.child_nodes = []
        self.metadata = []

    def init_node(self, tree_data_list: List[int]) -> List[int]:
        """ Takes a list of node data, and populates the node variables. """
        self.number_of_children = tree_data_list.pop(0)
        self.number_of_metadata = tree_data_list.pop(0)
        for i in range(self.number_of_children):
            new_node = TreeNode()
            tree_data_list = new_node.init_node(tree_data_list)
            self.child_nodes.append(new_node)
        self.metadata = tree_data_list[0:self.number_of_metadata]
        tree_data_list = tree_data_list[self.number_of_metadata:]
        return tree_data_list

    def get_node_value(self) -> int:
        """ Returns the value of the node. """
        node_value = 0

        if not self.child_nodes:
            node_value = sum(self.metadata)
        else:
            for meta_value in self.metadata:
                if meta_value <= len(self.child_nodes):
                    node_value += self.child_nodes[meta_value - 1].get_node_value()

        return node_value

    def sum_metadata(self) -> int:
        """ Returns the sum of all metadata from the node including all children. """
        child_metadata_sum = 0
        for child in self.child_nodes:
            child_metadata_sum += child.sum_metadata()
        child_metadata_sum += sum(self.metadata)
        return child_metadata_sum


def parse_input() -> List[str]:
    """ Reads the input file and returns a list of strings. """
    file_location = os.path.join(os.path.dirname(__file__), 'input.txt')
    input_values = []
    with open(file_location, 'r') as data:
        for line in data:
            input_values.append(line.strip())
    return input_values


# ============================ Part One ===============================


def part_one(input_data: List[str]):
    """ Puzzle Answer == 38567 """
    tree_data = list(map(int, input_data[0].split(' ')))
    root_node = TreeNode()
    root_node.init_node(tree_data)

    metadata_sum = root_node.sum_metadata()

    print(metadata_sum)


# ============================ Part Two ===============================


def part_two(input_data: List[str]):
    """ Puzzle Answer == 24453 """
    tree_data = list(map(int, input_data[0].split(' ')))
    root_node = TreeNode()
    root_node.init_node(tree_data)

    node_value = root_node.get_node_value()

    print(node_value)


# =====================================================================


if __name__ == '__main__':
    input_list = parse_input()
    part_one(input_list)
    part_two(input_list)
