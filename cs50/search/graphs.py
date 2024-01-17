from abc import ABC, abstractmethod
from collections import deque
from dataclasses import dataclass, field
from enum import Enum
from heapq import heapify, heappop, heappush, heappushpop
from typing import List, Sized


@dataclass(eq=True, frozen=True, order=True)
class State:
    row: int
    col: int


@dataclass(eq=True, frozen=True, order=True)
class Action:
    dr: int
    dc: int


@dataclass(eq=True, frozen=True, order=True)
class Node:
    state: State
    action: Action = field(default=None)
    parent: "Node" = field(default=None, repr=False)
    num_of_moves: int = 0


class Cells(Enum):
    EMPTY = 0
    INITIAL = 1
    GOAL = 2
    WALL = 3


class Frontier(ABC):
    def __init__(self) -> None:
        self.list: Sized = []
        self.visited_state: set[State] = set()

    def add(self, node: Node):
        self.visited_state.add(node.state)

    def pop(self):
        return self.list.pop()

    def is_visited(self, node: Node):
        return node.state in self.visited_state

    def is_empty(self):
        return len(self.list) == 0


class Search:
    ACTIONS = (
        Action(0, 1),
        Action(1, 0),
        Action(0, -1),
        Action(-1, 0),
    )

    def __init__(self, graph: tuple[tuple[Cells]]) -> None:
        self.graph = graph
        self.rows = len(graph)
        self.cols = len(graph[0])

        self.initial_state = [
            State(row, col)
            for row in range(self.rows)
            for col in range(self.cols)
            if self.graph[row][col] == Cells.INITIAL
        ][0]

        self.goal_state = [
            State(row, col)
            for row in range(self.rows)
            for col in range(self.cols)
            if self.graph[row][col] == Cells.GOAL
        ][0]

    def __allowed_cell(self, node: Node):
        row = node.state.row
        col = node.state.col

        return (
            row < self.rows
            and col < self.cols
            and row >= 0
            and col >= 0
            and self.graph[row][col] != Cells.WALL
        )

    def __is_terminal(self, node: Node) -> bool:
        if not self.__allowed_cell(node):
            raise Exception(f"{node} is not within bounds")

        return node.state == self.goal_state

    def __result(self, node: Node, action: Action):
        new_row = node.state.row + action.dr
        new_col = node.state.col + action.dc

        return Node(State(new_row, new_col), action, node, node.num_of_moves + 1)

    def __utility(self, node: Node):
        answer = []
        while node:
            answer.append(node)
            node = node.parent
        return answer

    def breadth_first(self) -> List[Node]:
        class QueueFrontier(Frontier):
            def __init__(self, initial_node: Node) -> None:
                super().__init__()
                self.list: deque[Node] = deque([initial_node])

            def add(self, node):
                self.list.appendleft(node)
                super().add(node)

        queue = QueueFrontier(Node(self.initial_state))
        return self.run(queue)

    def depth_first(self):
        class StackFrontier(Frontier):
            def __init__(self, initial_node: Node) -> None:
                super().__init__()
                self.list: List[Node] = [initial_node]

            def add(self, node):
                self.list.append(node)
                super().add(node)

        stack = StackFrontier(Node(self.initial_state))
        return self.run(stack)

    def a_star(self):
        class HeapFrontier(Frontier):
            def __heuristic_function(self, node: Node):
                return abs(self.goal_state.row - node.state.row) + abs(
                    self.goal_state.col - node.state.col
                )

            def __init__(self, initial_node: Node, goal_state: State) -> None:
                super().__init__()
                self.goal_state = goal_state
                self.list: List[Node] = [(0, initial_node)]
                heapify(self.list)

            def add(self, node: Node) -> None:
                heappush(
                    self.list,
                    (self.__heuristic_function(node) + node.num_of_moves, node),
                )

            def pop(self) -> Node:
                return (heappop(self.list))[1]

        heap_queue = HeapFrontier(Node(self.initial_state), self.goal_state)
        return self.run(heap_queue)

    def run(self, frontier: Frontier):
        while not frontier.is_empty():
            node = frontier.pop()

            if self.__is_terminal(node):
                return self.__utility(node)

            for action in self.ACTIONS:
                res = self.__result(node, action)

                if self.__allowed_cell(res) and not frontier.is_visited(res):
                    frontier.add(res)

        return []


graph = (
    (3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2),
    (3, 0, 3, 3, 3, 3, 3, 3, 3, 3, 3, 0),
    (3, 0, 3, 0, 0, 0, 0, 0, 0, 0, 3, 0),
    (3, 0, 3, 0, 3, 3, 3, 3, 3, 0, 3, 0),
    (3, 0, 0, 0, 3, 0, 0, 0, 0, 0, 3, 0),
    (3, 3, 3, 0, 3, 0, 3, 3, 3, 3, 3, 0),
    (1, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0),
)

graph = [[Cells(val) for val in row] for row in graph]

s = Search(graph)


print("\n--BREADTH FIRST SEARCH--")
for node in s.breadth_first():
    print(node)

print("\n--DEPTH FIRST SEARCH--")
for node in s.depth_first():
    print(node)

print("\n--A* SEARCH--")
for node in s.a_star():
    print(node)
