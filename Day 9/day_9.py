import os
import re
from collections import defaultdict
from typing import List

INPUT_REGEX = re.compile(r'(?P<players>[0-9]+) players; last marble is worth (?P<last>[0-9]+) points')


class LinkedListNode:
    """ Represents a node in a linked list. """

    def __init__(self, data, next_node=None, previous_node=None):
        self.data = data
        self.next = next_node
        self.previous = previous_node

    def get_previous(self, skip=0):
        """ Returns the previous node. Can skip a give number of nodes. """
        node = self.previous
        for i in range(skip):
            node = node.previous
        return node


class LoopedLinkedList:
    """ Represents a linked list, whose last node links back to the root node. """

    def __init__(self, data):
        self.root_node = LinkedListNode(data)
        self.root_node.next = self.root_node
        self.root_node.previous = self.root_node

    @staticmethod
    def insert_at_node(node, data):
        """ Inserts a new node at the position of the give node. """
        new_node = LinkedListNode(data, next_node=node, previous_node=node.previous)
        node.previous.next = new_node
        node.previous = new_node
        return new_node

    @staticmethod
    def delete_node(node):
        """ Removes the given node from the list. """
        node.previous.next = node.next
        node.next.previous = node.previous

    def insert_after_node(self, node, data, skip=0):
        """
        Inserts a new node at the position of the node that comes after the given node.

        Can skip a given number of nodes.
        """
        node = node.next
        for i in range(skip):
            node = node.next
        return self.insert_at_node(node, data)


class MarbleGame:
    """ Represents a game of marbles. """

    def __init__(self, number_of_players: int, last_marble_value: int):
        self.number_of_players = number_of_players
        self.last_marble_value = last_marble_value

        self.marble_circle = LoopedLinkedList(0)
        self.current_marble = self.marble_circle.root_node

        self.score_board = defaultdict(int)
        self.special_multiple = 23

    def play_game(self):
        """ Plays the game of marbles, keeping track of score. """
        for marble_count in range(1, self.last_marble_value + 1):
            if marble_count % self.special_multiple == 0:
                to_delete = self.current_marble.get_previous(skip=6)
                self.marble_circle.delete_node(to_delete)
                self.current_marble = to_delete.next
                self.score_board[marble_count % self.number_of_players] += marble_count + to_delete.data
            else:
                new_node = self.marble_circle.insert_after_node(self.current_marble, marble_count, skip=1)
                self.current_marble = new_node

    def highest_score(self):
        """ Returns the winning score for the game. """
        return max(self.score_board.values())


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
    """ Puzzle Answer == 370210 """
    match = INPUT_REGEX.match(input_data[0])

    players = int(match.groupdict()['players'])
    last = int(match.groupdict()['last'])
    marble_game = MarbleGame(players, last)
    marble_game.play_game()

    print(marble_game.highest_score())

# ============================ Part Two ===============================


def part_two(input_data: List[str]):
    """ Puzzle Answer == 3101176548 """
    match = INPUT_REGEX.match(input_data[0])

    players = int(match.groupdict()['players'])
    last = int(match.groupdict()['last']) * 100
    marble_game = MarbleGame(players, last)
    marble_game.play_game()

    print(marble_game.highest_score())


# =====================================================================


if __name__ == '__main__':
    input_list = parse_input()
    part_one(input_list)
    part_two(input_list)
