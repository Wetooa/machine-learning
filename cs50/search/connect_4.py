from dataclasses import dataclass, field
from itertools import chain
from math import inf
import numpy as np


@dataclass(eq=True, frozen=True)
class State:
    board: tuple[tuple[int]]


class Connect4:
    DISPLAY_CELLS = {
        0: " ",
        1: "X",
        -1: "O",
    }

    def __init__(self, rows=6, cols=7, connect=4) -> None:
        self.visited = {}
        self.rows = rows
        self.cols = cols
        self.connect = connect

    def __get_cells(self, state: State):
        return sum(1 for cell in list(chain(*state.board)) if cell)

    def __player(self, state: State):
        return 1 if self.__get_cells(state) % 2 == 0 else -1

    def __terminal(self, state: State):
        for i in range(self.rows):
            for j in range(self.cols - self.connect + 1):
                if state.board[i][j] and all(
                    [
                        state.board[i][j + k] == state.board[i][j]
                        for k in range(self.connect)
                    ]
                ):
                    return True

        for i in range(self.rows - self.connect + 1):
            for j in range(self.cols):
                if state.board[i][j] and all(
                    [
                        state.board[i + k][j] == state.board[i][j]
                        for k in range(self.connect)
                    ]
                ):
                    return True

        for i in range(self.rows - self.connect + 1):
            for j in range(self.cols - self.connect + 1):
                if state.board[i][j] and all(
                    [
                        state.board[i + k][j + k] == state.board[i][j]
                        for k in range(self.connect)
                    ]
                ):
                    return True

        for i in range(self.connect - 1, self.rows):
            for j in range(self.cols - self.connect + 1):
                if state.board[i][j] and all(
                    [
                        state.board[i - k][j + k] == state.board[i][j]
                        for k in range(self.connect)
                    ]
                ):
                    return True

        return self.__get_cells(state) == self.rows * self.cols

    def __utility(self, state: State):
        for i in range(self.rows):
            for j in range(self.cols - self.connect + 1):
                if state.board[i][j] and all(
                    [
                        state.board[i][j + k] == state.board[i][j]
                        for k in range(self.connect)
                    ]
                ):
                    return state.board[i][j]

        for i in range(self.rows - self.connect + 1):
            for j in range(self.cols):
                if state.board[i][j] and all(
                    [
                        state.board[i + k][j] == state.board[i][j]
                        for k in range(self.connect)
                    ]
                ):
                    return state.board[i][j]

        for i in range(self.rows - self.connect + 1):
            for j in range(self.cols - self.connect + 1):
                if state.board[i][j] and all(
                    [
                        state.board[i + k][j + k] == state.board[i][j]
                        for k in range(self.connect)
                    ]
                ):
                    return state.board[i][j]

        for i in range(self.connect - 1, self.rows):
            for j in range(self.cols - self.connect + 1):
                if state.board[i][j] and all(
                    [
                        state.board[i - k][j + k] == state.board[i][j]
                        for k in range(self.connect)
                    ]
                ):
                    return state.board[i][j]

        return 0

    def __actions(self, state: State):
        return [j for j in range(self.cols) if state.board[0][j] == 0]

    def __result(self, state: State, cell_column: int):
        def index_of_first(lst, pred):
            for i, v in enumerate(lst):
                if pred(v):
                    return i
            return len(lst)

        cell_row = (
            index_of_first(list(zip(*state.board[::]))[cell_column], pred=lambda x: x)
            - 1
        )

        return State(
            board=tuple(
                tuple(
                    state.board[i][j]
                    if i != cell_row or j != cell_column
                    else self.__player(state)
                    for j in range(self.cols)
                )
                for i in range(self.rows)
            )
        )

    def __minimax(self, state: State, a, b):
        return (a < b) if self.__player(state) == 1 else (a > b)

    def __find_best_move(self, state: State):
        if self.__terminal(state):
            return (self.__utility(state), None)

        if state not in self.visited:
            self.visited[state] = (-inf if self.__player(state) == 1 else inf, None)
            for action in self.__actions(state):
                util, _ = self.__find_best_move(self.__result(state, action))
                if self.__minimax(state, self.visited[state][0], util):
                    self.visited[state] = (util, action)
        return self.visited[state]

    def display(self, state: State):
        print(
            np.matrix(
                [
                    [self.DISPLAY_CELLS[state.board[i][j]] for j in range(self.cols)]
                    for i in range(self.rows)
                ]
            )
        )

    def play(self):
        state = State(
            board=tuple(tuple(0 for _ in range(self.cols)) for _ in range(self.rows))
        )

        while not self.__terminal(state):
            move = None
            if self.__player(state) == 1:
                self.display(state)
                move = int(input("Enter column to place: "))
            else:
                _, move = self.__find_best_move(state)
            state = self.__result(state, move)

        winner = self.__utility(state)
        self.display(state)
        if winner == 0:
            print("It's a draw!")
        else:
            print(f"The winner is {1 if winner == 1 else 2}!!!")


c = Connect4()
c.play()
