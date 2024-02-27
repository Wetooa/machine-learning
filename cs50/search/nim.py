from dataclasses import dataclass
from math import inf


@dataclass(eq=True, frozen=True)
class State:
    pebbles: int = 20
    turn: int = 0


class Nim:
    def __init__(self) -> None:
        self.visited = {}

    def __actions(self):
        return [1, 2]

    def __result(self, state: State, action: int):
        return State(state.pebbles - action, state.turn ^ 1)

    def __is_terminal(self, state: State):
        return state.pebbles <= 2

    def __utility(self, state: State):
        return 1 if state.turn else -1

    def __minimax(self, state: State, a, b):
        return (a < b) ^ state.turn

    def __find_best_move(self, state: State):
        if self.__is_terminal(state):
            return (self.__utility(state), None)

        if state not in self.visited:
            self.visited[state] = (-inf if state.turn == 0 else inf, None)
            for action in self.__actions():
                util, _ = self.__find_best_move(self.__result(state, action))
                if self.__minimax(state, self.visited[state][0], util):
                    self.visited[state] = (util, action)

        return self.visited[state]

    def play(self, state: State = State()):
        while not self.__is_terminal(state):
            if state.turn == 0:
                print(f"Pebble count: {state.pebbles}")
                state = self.__result(state, int(input("Enter choice (1 or 2): ")))
            else:
                _, action = self.__find_best_move(state)
                print(f"Ai's turn - Chooses {action}")
                state = self.__result(state, action)

        print(f"Winner is player {'1' if self.__utility(state) == 1 else '2 (AI)'}")


nim = Nim()
nim.play(State(30, 1))


# 20 -> [1, 2]
