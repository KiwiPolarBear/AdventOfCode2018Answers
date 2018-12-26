import os
import re
import string
from typing import List, Set

import math

INSTRUCTION_RE = re.compile(
    r'Step (?P<before>[A-Z]) must be finished before step (?P<after>[A-Z]) can begin.'
)


class TaskNode:
    """ Represents a task to be executed. """

    name: str
    before_tasks: Set['TaskNode']
    next_tasks: Set['TaskNode']
    time_started: int

    def __init__(self, name, base_length):
        self.name = name
        self.base_length = base_length
        self.before_tasks = set()
        self.next_tasks = set()
        self.time_started = 0

    def time_left(self, current_time):
        """ Returns the length the task will take. """
        total_length = string.ascii_uppercase.find(self.name) + self.base_length + 1
        return total_length - (current_time - self.time_started)

    def can_execute(self, current_task_order: str) -> bool:
        """ Checks if the task can be executed, given the tasks that have already run. """
        for task in self.before_tasks:
            if task.name not in current_task_order:
                return False
        return True


class TaskNodeExecutor:
    """ Executes TaskNodes in the correct order. """

    available_tasks: Set[TaskNode]
    available_workers: int
    executed_tasks: str

    def __init__(self, available_tasks: Set[TaskNode]):
        self.available_tasks = available_tasks
        self.available_workers = 0
        self.executed_tasks = ''

    def execute_task(self, task: TaskNode):
        """ Executes a task, and adds its next tasks to available tasks. """
        self.executed_tasks += task.name
        for item in task.next_tasks:
            self.available_tasks.add(item)

    def get_next_task(self) -> TaskNode:
        """ Returns the next executable task. """
        next_task = None
        executable_tasks = [task for task in self.available_tasks if task.can_execute(self.executed_tasks)]
        if executable_tasks:
            executable_tasks.sort(key=lambda x: x.name)
            next_task = executable_tasks[0]
        return next_task

    def execute_all_tasks(self) -> str:
        """ Executes all tasks and returns the oder they were run in. """
        while self.available_tasks:
            next_task = self.get_next_task()
            self.available_tasks.remove(next_task)
            self.execute_task(next_task)
        return self.executed_tasks

    def execute_all_tasks_divided(self, num_of_workers: int) -> int:
        """ Divides tasks between given workers and executes based on time. """
        self.available_workers = num_of_workers
        total_time = 0
        tasks_in_progress = []
        while self.available_tasks or tasks_in_progress:

            shortest_time_left = math.inf
            tasks_in_progress.sort(key=lambda x: x.time_left(total_time), reverse=False)

            # Finish tasks in progress.
            for task in tasks_in_progress:
                if task.time_left(total_time) <= shortest_time_left:
                    shortest_time_left = task.time_left(total_time)
                    self.available_workers += 1
                    self.execute_task(task)
                    tasks_in_progress.remove(task)

            if shortest_time_left != math.inf:
                total_time += shortest_time_left

            # Assign workers to tasks
            next_task = self.get_next_task()
            while self.available_workers and next_task:
                self.available_tasks.remove(next_task)
                tasks_in_progress.append(next_task)
                self.available_workers -= 1
                next_task.time_started = total_time
                next_task = self.get_next_task()

        return total_time


class DefaultTaskDict(dict):
    """ A dictionary that returns an instantiated TaskNode by default. """

    def __missing__(self, key: str):
        res = self[key] = TaskNode(key, 60)
        return res


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
    """ Puzzle Answer == CFMNLOAHRKPTWBJSYZVGUQXIDE """
    task_node_dict = DefaultTaskDict()

    for instruction in input_data:
        group_dict = INSTRUCTION_RE.match(instruction).groupdict()
        before = task_node_dict[group_dict['before']]
        after = task_node_dict[group_dict['after']]
        before.next_tasks.add(after)
        after.before_tasks.add(before)

    available_tasks = set(task for task in task_node_dict.values() if not task.before_tasks)
    executor = TaskNodeExecutor(available_tasks)
    task_order = executor.execute_all_tasks()

    print(task_order)


# ============================ Part Two ===============================


def part_two(input_data: List[str]):
    """ Puzzle Answer == 971 """
    task_node_dict = DefaultTaskDict()

    for instruction in input_data:
        group_dict = INSTRUCTION_RE.match(instruction).groupdict()
        before = task_node_dict[group_dict['before']]
        after = task_node_dict[group_dict['after']]
        before.next_tasks.add(after)
        after.before_tasks.add(before)

    available_tasks = set(task for task in task_node_dict.values() if not task.before_tasks)
    executor = TaskNodeExecutor(available_tasks)
    task_execution_time = executor.execute_all_tasks_divided(5)

    print(task_execution_time)


# =====================================================================


if __name__ == '__main__':
    input_list = parse_input()
    part_one(input_list)
    part_two(input_list)
