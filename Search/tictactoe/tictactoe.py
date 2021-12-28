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

    # Check if it is in the initial game state
    moves = 0
    for row in board:
        for column in row:
            if column != None:
                moves += 1

    if moves % 2 == 0:
        return X
    elif moves % 2 == 1:
        return O
            
    # raise NotImplementedError


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """

    actions = set()
    for i, row in enumerate(board):
        for j, column in enumerate(row):
            if column == None:
                actions.add((i, j))
    
    return actions

    # raise NotImplementedError


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if action not in actions(board):
        raise ValueError('The action is invalid.')

    result = copy.deepcopy(board)
    result[action[0]][action[1]] = player(board)
    return result
    # raise NotImplementedError


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """

    # Checking for horizontal match
    for row in board:
        if len(set(row)) == 1:
            if row[0] != None:             
                return row[0]
    
    # Checking for vertical match
    new_board = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    for i, row in enumerate(board):
        for j, column in enumerate(row):
            new_board[j][i] = column

    for column in new_board:
        if len(set(column)) == 1:
            if column[0] != None:
                return column[0]

    # Checking for diagonal match
    left_diagonal = [board[0][0], board[1][1], board[2][2]]
    right_diagonal = [board[0][2], board[1][1], board[2][0]]
    
    if len(set(left_diagonal)) == 1:
        if left_diagonal[0] != None:
            return left_diagonal[0]
    elif len(set(right_diagonal)) == 1:
        if right_diagonal[0] != None: 
            return right_diagonal[0]
    
    # if in progress or ended in tie
    return None

    # raise NotImplementedError


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    # if the game is in progress
    if winner(board) == None:
        # if all cells have not been filled
        for row in board:
            for column in row:
                if column == None:
                    return False
        return True        
    else:
        return True
    
    # raise NotImplementedError


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    result = winner(board)
    if result == 'X':
        return 1
    elif result == 'O':
        return -1
    else:
        return 0
    
    # raise NotImplementedError

def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None

    action_value = choose_action(board)
    return action_value[0]
    # raise NotImplementedError

def choose_action(board):
    turn = player(board)
    child_boards = []
    for action in actions(board):
        child_boards.append(result(board, action))
    
    values = {-1: [], 0: [], 1: []}
    for child_board in child_boards:    
        if terminal(child_board):
            values[utility(child_board)].append(child_board)
            # (optimization) break immediately if the best value for the player is found
            if turn == X and utility(child_board) == 1:
                break 
            elif turn == O and utility(child_board) == -1:
                break 
            else:
                continue

        action_value = choose_action(child_board)
        values[action_value[1]].append(child_board)

    available_values = []
    for key in values:
        if values[key] != []:
            available_values.append(key)

    # print(values, available_values)
    for action in actions(board):
        if turn == X and result(board, action) == values[max(available_values)][0]:
            return (action, max(available_values))
        elif turn == O and result(board, action) == values[min(available_values)][0]:
            return (action, min(available_values))