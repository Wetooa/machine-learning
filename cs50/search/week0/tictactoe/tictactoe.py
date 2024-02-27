"""
Tic Tac Toe Player
"""

import math
import itertools 

X = "X"
O = "O"
EMPTY = None


def initial_state():
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    return O if sum(cell != EMPTY for cell in list(itertools.chain(*board))) % 2 else X


def actions(board):
    actions = []
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY: actions.append((i, j))
    return actions



def result(board, action):
    r, c = action
    return [[board[i][j] if i != r or j != c else player(board) for j in range(3)] for i in range(3)]


def winner(board):
    return player(board) if utility(board) else None


def terminal(board) -> bool:
    return utility(board) or all(cell != EMPTY for row in board for cell in row)


def utility(board):
    res = None

    for row in board:
        if row[0] != EMPTY and all(cell == row[0] for cell in row): res = row[0]
    for row in zip(*board):
        if row[0] != EMPTY and all(cell == row[0] for cell in row): res = row[0]
    if board[1][1] != EMPTY and (board[0][0] == board[1][1] == board[2][2] or board[0][2] == board[1][1] == board[2][0]): res = board[1][1]

    return 1 if res == X else -1 if res == O else 0

def dfs(board):

    if terminal(board):
        return (utility(board), None)
    
    current, best_move = -math.inf if player(board) == X else math.inf, None
    
    for action in actions(board):
        new_state = result(board, action)
        util, move = dfs(new_state)

        if ((current < util) if player(board) == X else (current > util)): 
            current = util
            best_move = action

    return (current, best_move)


def minimax(board):
    return dfs(board)[1]
