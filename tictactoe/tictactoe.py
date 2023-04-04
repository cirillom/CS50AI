"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    x_count = sum(row.count(X) for row in board)
    o_count = sum(row.count(O) for row in board)

    if x_count == o_count:
        return X
    else:
        return O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    available_actions = []

    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                action = (i, j)
                available_actions.append(action)
    return available_actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    new_board = copy.deepcopy(board)
    if new_board[action[0]][action[1]] != EMPTY:
        raise ValueError("Invalid action")
    
    new_board[action[0]][action[1]] = player(board)
    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    for row in board:
        if row.count(X) == 3:
            return X
        elif row.count(O) == 3:
            return O
    
    for i in range(3):
        column = [board[j][i] for j in range(3)]
        if column.count(X) == 3:
            return X
        elif column.count(O) == 3:
            return O
    
    if board[0][0] == board[1][1] == board[2][2]:
        return board[0][0]
    elif board[0][2] == board[1][1] == board[2][0]:
        return board[0][2]
    
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) != None:
        return True
    
    if sum(row.count(EMPTY) for row in board) == 0:
        return True
    
    return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X:
        return 1
    
    if winner(board) == O:
        return -1
    
    return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if player(board) == X:
        return max_val(board, -math.inf, math.inf)[0]
    else:
        return min_val(board, -math.inf, math.inf)[0]


def max_val(board, alpha, beta):
    if terminal(board):
        return (None, utility(board))
    val = -math.inf
    best_action = None

    for action in actions(board):
        next_board = result(board, action)
        next_val = min_val(next_board, alpha, beta)[1]
        if next_val > val:
            val = next_val
            best_action = action

        #pruning
        alpha = max(alpha, val)
        if alpha >= beta:
            break


    return (best_action, val)


def min_val(board, alpha, beta):
    if terminal(board):
        return (None, utility(board))
    val = math.inf
    best_action = None

    for action in actions(board):
        next_board = result(board, action)
        next_val = max_val(next_board, alpha, beta)[1]
        if next_val < val:
            val = next_val
            best_action = action

        #pruning
        beta = min(val, beta)
        if beta <= alpha:
            break

    return (best_action, val)
