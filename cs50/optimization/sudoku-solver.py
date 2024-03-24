from sudoku import Sudoku


class SudokuSolver:

    def __init__(self) -> None:
        self.board = Sudoku(3).difficulty(0.5)
        self.board.show()

        self.board = self.board.solve()
        self.board.show()

    def solve(self):
        self.search()

    def possible(self, r, c, n):
        if any([cell == n for cell in self.board.board[r]]):
            return False
        if any([cell == n for cell in list(zip(*self.board))[c]]):
            return False
        for i in range(r // 3 * 3, r // 3 * 3 + 3):
            for j in range(c // 3 * 3, c // 3 * 3 + 3):
                if self.board.board[i][j] == n:
                    return False
        return True

    def search(self):

        for r in range(9):
            for c in range(9):
                if self.board.board[r][c] == 0:
                    for n in range(1, 10):
                        if self.possible(r, c, n):
                            self.board.board[r][c] = n
                            self.search()
                            self.board.board[r][c] = 0

        self.board.show()


s = SudokuSolver()
