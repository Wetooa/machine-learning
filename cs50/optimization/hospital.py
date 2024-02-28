from collections import defaultdict
from math import inf
from random import sample


class Space:

    NEIGHBOR_DIRECTIONS = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    def __init__(self, rows, cols, num_of_hospitals) -> None:
        self.rows = rows
        self.cols = cols
        self.num_of_hospitals = num_of_hospitals

        self.hospitals = set()
        self.houses = set()

    def add_house(self, row, col):
        self.houses.add((row, col))

    def add_hospital(self, row, col):
        self.hospitals.add((row, col))

    def get_cost(self, houses):
        cost = defaultdict(lambda: inf)

        for house_x, house_y in houses:
            for hospital in self.hospitals:
                hospital_x, hospital_y = hospital
                cost[hospital] = min(
                    cost[hospital],
                    abs(house_x - hospital_x) + abs(house_y - hospital_y),
                )

        return sum(cost.values())

    def get_random_state(self, num_houses):
        self.hospitals = set(
            sample(
                [
                    (row, col)
                    for row in self.rows
                    for col in self.cols
                    if (row, col) not in self.hospitals
                ],
                num_houses,
            )
        )

    def get_neighbors(self, houses):
        neighbors = set()

        for house_x, house_y in houses:

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
                    copy = set(houses)
                    copy.add((r, c))
                    copy.remove((r, c))
                    neighbors.add(copy)

        return neighbors

    def hill_climb(self, maximum, log):

        self.get_random_state(maximum)
        current_best = self.get_cost(self.houses)

        print("Initial best state cost:", current_best)

        while True:
            new_best = current_best
            for neighbor in self.get_neighbors(self.houses):
                new_best = max(new_best, self.get_cost(neighbor))

            if new_best <= current_best:
                break

            print("New best state:", current_best)
