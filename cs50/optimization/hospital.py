from collections import defaultdict
from math import dist, inf
from random import sample, randrange

import numpy as np
from PIL import Image


class Space:
    NEIGHBOR_DIRECTIONS = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    def __init__(self, rows, cols, num_of_hospitals, num_of_houses) -> None:
        self.rows = rows
        self.cols = cols
        self.num_of_hospitals = num_of_hospitals
        self.num_of_houses = num_of_houses

        self.hospitals: list = self.get_random_hospital_state()
        self.houses: list = []

    def add_house(self, row, col):
        self.houses.append((row, col))

    def add_hospital(self, row, col):
        self.hospitals.append((row, col))

    def get_cost(self, houses=None) -> int:
        if not houses:
            houses = self.houses

        cost: defaultdict[int, int] = defaultdict(lambda: 10**10)

        for house in houses:
            house_x, house_y = house
            for hospital in self.hospitals:
                hospital_x, hospital_y = hospital
                cost[house] = min(
                    cost[house],
                    abs(house_x - hospital_x) + abs(house_y - hospital_y),
                )

        return sum(cost.values())

    def get_random_hospital_state(self):
        return list(
            sample(
                [(row, col) for row in range(self.rows) for col in range(self.cols)],
                self.num_of_hospitals,
            )
        )

    def get_random_houses_state(self):
        return list(
            sample(
                [
                    (row, col)
                    for row in range(self.rows)
                    for col in range(self.cols)
                    if (row, col) not in self.hospitals
                ],
                self.num_of_houses,
            )
        )

    def get_neighbors(self, houses=None) -> list[list]:
        if not houses:
            houses = self.houses

        neighbors = []

        for house_x, house_y in houses:
            copy = list(houses)
            copy.remove((house_x, house_y))

            for dx, dy in self.NEIGHBOR_DIRECTIONS:
                r = house_x + dx
                c = house_y + dy
                if (
                    r >= 0
                    and c >= 0
                    and r < self.rows
                    and c < self.cols
                    and (r, c) not in self.hospitals
                    and (r, c) not in self.houses
                    and (r, c) not in neighbors
                ):
                    copy.append((r, c))
                    neighbors.append(list(copy))
                    copy.remove((r, c))

        return neighbors

    def random_restart(self, iterations=10):
        best_house_state = self.get_random_houses_state()
        self.houses = best_house_state
        self.display()

        while iterations:
            self.hill_climb()
            iterations -= 1

            if self.get_cost() < self.get_cost(best_house_state):
                best_house_state = list(self.houses)

            print(f"Current best state (cost={self.get_cost(best_house_state)})")

        self.houses = best_house_state
        self.display()

    def hill_climb(self, maximum=None, log=False):
        self.houses = self.get_random_houses_state()

        if log:
            print("Initial best state cost:", self.get_cost())

        while True:
            best_neighbor = min(
                self.get_neighbors(), key=lambda x: self.get_cost(houses=x)
            )
            if self.get_cost(best_neighbor) >= self.get_cost():
                break
            self.houses = list(best_neighbor)
            if log:
                print("New best state:", self.get_cost())
                self.display()

        if log:
            print(f"Best state is: {self.get_cost()}")
            self.display()

    def display(self):
        space = [[0] * self.cols for _ in range(self.rows)]

        for r, c in self.hospitals:
            space[r][c] = 1
        for r, c in self.houses:
            space[r][c] = 2

        for r in range(self.rows):
            for c in range(self.cols):
                print(
                    "H" if space[r][c] == 1 else "O" if space[r][c] == 2 else " ",
                    end=" ",
                )
            print()


s = Space(rows=10, cols=30, num_of_hospitals=10, num_of_houses=20)

hospitals = s.random_restart()
