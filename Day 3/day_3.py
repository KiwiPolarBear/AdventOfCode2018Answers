import os
import re
from typing import List


class FabricClaim:
    """ An elf's claim on santa's special fabric. """

    string_regex = (
        r'^#(?P<claim_id>[0-9]+) @ '
        r'(?P<from_left>[0-9]+),'
        r'(?P<from_top>[0-9]+): '
        r'(?P<width>[0-9]+)x'
        r'(?P<height>[0-9]+)$'
    )

    def __init__(self, claim_id: int, from_left: int, from_top: int, width: int, height: int):
        self.claim_id = claim_id
        self.from_left = from_left
        self.from_top = from_top
        self.width = width
        self.height = height

    @classmethod
    def from_string(cls, data: str) -> 'FabricClaim':
        match = re.match(cls.string_regex, data)
        if not match:
            raise ValueError(f'Value does not match regex `{cls.string_regex}`')

        # Convert values to integers.
        group_dict = {key: int(val) for key, val in match.groupdict().items()}

        return cls(**group_dict)


class SpecialFabric:
    """ Represents the special piece of fabric. """

    def __init__(self):
        self.fabric_dict = {}

    def apply_claim(self, claim: FabricClaim):
        """
        Calculates the unique id for each square the fabric occupies,
        and adds the claim to a dictionary.
        """
        for i in range(claim.width):
            for n in range(claim.height):
                square_id = f'{i + claim.from_left}x{n + claim.from_top}'
                if square_id in self.fabric_dict:
                    self.fabric_dict[square_id].append(claim)
                else:
                    self.fabric_dict[square_id] = [claim]

    def count_overlaps(self) -> int:
        """
        Returns the number of squares in the fabric dictionary,
        that have more then one claim associated with them.
        """
        total = 0
        for claim_list in self.fabric_dict.values():
            if len(claim_list) >= 2:
                total += 1
        return total

    def find_clean_claim(self) -> int:
        """" Finds the id of the one claim that does not intersect with any others. """
        dirty_claim_ids = []
        clean_claim_ids = []
        for claim_list in self.fabric_dict.values():
            if len(claim_list) >= 2:
                dirty_claim_ids.extend([claim.claim_id for claim in claim_list])
            else:
                clean_claim_ids.extend([claim.claim_id for claim in claim_list])
        diff = set(dirty_claim_ids).symmetric_difference(set(clean_claim_ids))
        return diff.intersection(clean_claim_ids).pop()


def parse_input() -> List[FabricClaim]:
    """ Reads the input file and returns a list of FabricClaims. """
    file_location = os.path.join(os.path.dirname(__file__), 'input.txt')
    input_values = []
    with open(file_location, 'r') as data:
        for line in data:
            input_values.append(FabricClaim.from_string(line.strip()))
    return input_values


# ============================ Part One ===============================


def part_one(input_data: List[FabricClaim]):
    """ Puzzle Answer == 103806 """
    fabric = SpecialFabric()
    for claim in input_data:
        fabric.apply_claim(claim)
    print(fabric.count_overlaps())


# ============================ Part Two ===============================


def part_two(input_data: List[FabricClaim]):
    """ Puzzle Answer == 625 """
    fabric = SpecialFabric()
    for claim in input_data:
        fabric.apply_claim(claim)
    print(fabric.find_clean_claim())


# =====================================================================

if __name__ == '__main__':
    input_list = parse_input()
    part_one(input_list)
    part_two(input_list)
