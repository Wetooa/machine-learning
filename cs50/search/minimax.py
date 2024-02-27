from abc import ABC, abstractmethod
from copy import deepcopy
from dataclasses import dataclass
from enum import Enum
from itertools import chain
from math import inf

import numpy as np


@dataclass
class Coordinate:
    row: int
    col: int


class TicTacToe:
    def __init__(self, rows: int = 3, cols: int = 3) -> None:
        self.board = [[0 for _ in range(cols)] for _ in range(rows)]
        self.rows = rows
        self.cols = cols
        self.visited = {}
        self.turn = 1

    def reset(self):
        self.board = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        self.visited = {}
        self.turn = 1

    def __is_terminal(self):
        if all(cell for cell in chain(*self.board)):
            return True
        if any(all(cell and cell == row[0] for cell in row) for row in self.board):
            return True
        if any(
            (all(cell and cell == row[0] for cell in row))
            for row in zip(*self.board[::-1])
        ):
            return True

        return self.board[1][1] and (
            self.board[0][0] == self.board[1][1] == self.board[2][2]
            or self.board[0][2] == self.board[1][1] == self.board[2][0]
        )

    def __utility(self):
        for row in self.board:
            if row[0] and all(cell and cell == row[0] for cell in row):
                return row[0]

        for row in zip(*self.board[::-1]):
            if row[0] and all(cell == row[0] for cell in row):
                return row[0]

        return (
            self.board[1][1]
            if self.board[1][1]
            and (
                self.board[0][0] == self.board[1][1] == self.board[2][2]
                or self.board[0][2] == self.board[1][1] == self.board[2][0]
            )
            else 0
        )

    def __result(self, action: Coordinate):
        self.board[action.row][action.col] = self.__player()
        self.turn *= -1

    def __undo_action(self, action: Coordinate):
        self.board[action.row][action.col] = 0
        self.turn *= -1

    def __player(self):
        return self.turn

    def __actions(self):
        actions = []
        for row in range(self.rows):
            for col in range(self.cols):
                if self.board[row][col] == 0:
                    actions.append(Coordinate(row, col))
        return actions

    def __hash_state(self):
        return tuple(tuple(row) for row in self.board)

    def __minmax_compare(self, a: int, b: int):
        return (a < b) ^ (1 if self.__player() == 1 else 0)

    def __find_best_move(self):
        def dfs():
            if self.__is_terminal():
                return (self.__utility(), None)

            hashed = self.__hash_state()

            if hashed not in self.visited:
                self.visited[hashed] = (-1 * self.__player() * inf, None)
                for action in self.__actions():
                    self.__result(action)
                    util, _ = dfs()
                    if self.__minmax_compare(self.visited[hashed][0], util):
                        self.visited[hashed] = (util, action)
                    self.__undo_action(action)

            return self.visited[hashed]

        _, coor = dfs()
        return coor

    def display(self):
        print(f"--- PLAYER {1 if self.__player() == 1 else 2} ---")
        print(
            np.matrix(
                [
                    ["X" if cell == 1 else "O" if cell == -1 else "_" for cell in row]
                    for row in self.board
                ]
            ),
            end="\n\n",
        )

    def singleplayer_play(self):
        while not self.__is_terminal():
            if self.__player() == 1:
                self.display()
                user_input = input(
                    "Enter row and column (0-indexed, ex. 0 0): "
                ).split()
                self.__result(Coordinate(*map(int, user_input)))
            else:
                self.__result(self.__find_best_move())

        self.display()
        winner = self.__utility()

        if winner == 0:
            print("Draw!")
        else:
            print(f"Winner is player {1 if winner == 1 else '2 (AI)'}")

    def ai_play(self):
        while not self.__is_terminal():
            self.__result(self.__find_best_move())
            self.display()

        self.display()
        winner = self.__utility()

        if winner == 0:
            print("Draw!")
        else:
            print(f"Winner is player {1 if winner == 1 else -1}")


tik = TicTacToe()
tik.singleplayer_play()
# tik.ai_play()
