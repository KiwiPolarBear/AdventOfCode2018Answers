import os
import re
from collections import defaultdict, Counter
from typing import List, Dict


class Guard:
    """ Represents one of santa's guards. """

    guard_begin_regex = (
        r'^\[(?P<date>[0-9]+-[0-9]+-[0-9]+) '
        r'(?P<time>[0-9]+:[0-9]+)\] '
        r'Guard #(?P<guard_id>[0-9]+) begins shift$'
    )

    falls_asleep_regex = (
        r'^\[(?P<date>[0-9]+-[0-9]+-[0-9]+) '
        r'(?P<time>[0-9]+:[0-9]+)\] falls asleep$'
    )

    wakes_up_regex = (
        r'^\[(?P<date>[0-9]+-[0-9]+-[0-9]+) '
        r'(?P<time>[0-9]+:[0-9]+)\] wakes up$'
    )

    def __init__(self, guard_id: int):
        self.guard_id = guard_id
        self.sleep_dict = defaultdict(lambda: defaultdict(lambda: False))
        self._total_sleep = None
        self._minute_most_slept = None
        self._most_slept_frequency = None

    @property
    def total_sleep(self) -> int:
        if not self._total_sleep:
            self.calculate_total_sleep()
        return self._total_sleep

    @property
    def minute_most_slept(self) -> int:
        if not self._minute_most_slept:
            self.calculate_minute_most_slept()
        return self._minute_most_slept

    @property
    def minute_frequency(self) -> int:
        if not self._most_slept_frequency:
            self.calculate_minute_most_slept()
        return self._most_slept_frequency

    def calculate_total_sleep(self):
        """ Calculates and stores the total minutes slept. """
        self._total_sleep = 0
        if len(self.sleep_dict) > 0:
            for time_dict in self.sleep_dict.values():
                self._total_sleep += sum(time_dict.values())

    def calculate_minute_most_slept(self):
        """ Calculates and stores the minute most slept, and its frequency. """
        minute_dict = defaultdict(int)
        for time_dict in self.sleep_dict.values():
            for minute, did_sleep in time_dict.items():
                minute_dict[minute] += 1 if did_sleep else 0

        most_common = Counter(minute_dict).most_common(1)[0]
        self._minute_most_slept, self._most_slept_frequency = most_common

    def apply_sleep(self, start_minute: int, end_minute: int, date: str):
        """
        Takes the minute fell asleep, and minute awoke,
        and adds the sleep minutes to the sleep dict on the given date.
        """
        for i in range(start_minute, end_minute):
            self.sleep_dict[date][i] = True


def parse_input() -> List[str]:
    """ Reads the input file and returns a list of strings. """
    file_location = os.path.join(os.path.dirname(__file__), 'input.txt')
    input_values = []
    with open(file_location, 'r') as data:
        for line in data:
            input_values.append(line.strip())
    return input_values


def parse_guard_data(input_data: List[str]) -> Dict[int, Guard]:
    """
    Parses the guard sleep data, into Guard instances.

    Only returns guards who have actually slept on their shift.
    """
    guard_dict = {}
    active_guard = None
    last_asleep_match = None

    for line in input_data:
        if re.match(Guard.guard_begin_regex, line):
            guard_match = re.match(Guard.guard_begin_regex, line)

            new_guard_id = int(guard_match.groupdict()['guard_id'])
            if new_guard_id in guard_dict:
                active_guard = guard_dict[new_guard_id]
            else:
                active_guard = Guard(int(new_guard_id))
                guard_dict[active_guard.guard_id] = active_guard

        elif re.match(Guard.falls_asleep_regex, line):
            # We know the next line is about the guard waking up.
            last_asleep_match = re.match(Guard.falls_asleep_regex, line)
        else:
            # We know the previous line was about the guard falling asleep.
            wake_up_match = re.match(Guard.wakes_up_regex, line)

            date = last_asleep_match.groupdict()['date']
            sleep_time = int(last_asleep_match.groupdict()['time'].split(':')[1])
            wake_time = int(wake_up_match.groupdict()['time'].split(':')[1])
            active_guard.apply_sleep(sleep_time, wake_time, date)

    return {k: v for k, v in guard_dict.items() if v.total_sleep}


# ============================ Part One ===============================


def part_one(input_data: List[str]):
    """ Puzzle Answer == 95199 """
    guard_dict = parse_guard_data(input_data)

    minutes_dict = dict(map(lambda x: (x[0], x[1].total_sleep), guard_dict.items()))
    guard_id, _ = Counter(minutes_dict).most_common(1)[0]
    print(guard_id * guard_dict[guard_id].minute_most_slept)


# ============================ Part Two ===============================


def part_two(input_data: List[str]):
    """ Puzzle Answer == 7887 """
    guard_dict = parse_guard_data(input_data)

    minutes_dict = dict(map(lambda x: (x, x.minute_frequency), guard_dict.values()))
    guard, _ = Counter(minutes_dict).most_common(1)[0]
    print(guard.guard_id * guard.minute_most_slept)


# =====================================================================


if __name__ == '__main__':
    input_list = parse_input()
    input_list.sort()
    part_one(input_list)
    part_two(input_list)
