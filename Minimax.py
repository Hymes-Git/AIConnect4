import numpy as np
import random

def minimax_move(board, top_row, available_moves, current_player, depth=4):
    if not available_moves:
        return -1
    if len(available_moves) == 1:
        return available_moves[0]

    best_score = float('-inf')
    best_moves = []

    for col in available_moves:
        new_board = [column[:] for column in board]
        new_top_row = top_row[:]
        row = new_top_row[col]
        new_board[col][row] = current_player
        new_top_row[col] -= 1

        new_available_moves = available_moves.copy()
        if new_top_row[col] < 0:
            new_available_moves.remove(col)

        opponent = 1 if current_player == 2 else 2

        if check_win(new_board, col, row, current_player):
            return col 

        score = min_value(new_board, new_top_row, new_available_moves, depth - 1, current_player, opponent)

        if score > best_score:
            best_score = score
            best_moves = [col]
        elif score == best_score:
            best_moves.append(col)

    return random.choice(best_moves)

def max_value(board, top_row, available_moves, depth, original_player, current_player):
    if depth == 0 or not available_moves:
        return evaluate_board(board, original_player)

    value = float('-inf')
    for col in available_moves:
        new_board = [column[:] for column in board]
        new_top_row = top_row[:]
        row = new_top_row[col]
        new_board[col][row] = current_player
        new_top_row[col] -= 1

        new_available_moves = available_moves.copy()
        if new_top_row[col] < 0:
            new_available_moves.remove(col)

        if check_win(new_board, col, row, current_player):
            return 1000 if current_player == original_player else -1000

        opponent = 1 if current_player == 2 else 2
        value = max(value, min_value(new_board, new_top_row, new_available_moves, depth - 1, original_player, opponent))

    return value

def min_value(board, top_row, available_moves, depth, original_player, current_player):
    if depth == 0 or not available_moves:
        return evaluate_board(board, original_player)

    value = float('inf')
    for col in available_moves:
        new_board = [column[:] for column in board]
        new_top_row = top_row[:]
        row = new_top_row[col]
        new_board[col][row] = current_player
        new_top_row[col] -= 1

        new_available_moves = available_moves.copy()
        if new_top_row[col] < 0:
            new_available_moves.remove(col)

        if check_win(new_board, col, row, current_player):
            return 1000 if current_player == original_player else -1000

        opponent = 1 if current_player == 2 else 2
        value = min(value, max_value(new_board, new_top_row, new_available_moves, depth - 1, original_player, opponent))

    return value

def check_win(board, col, row, player, connect_num=4):
    x_dimension = len(board)
    y_dimension = len(board[0])
    
    # check horizontal
    in_row = 1
    # check right
    for num in range(1, connect_num):
        if col + num < x_dimension and board[col + num][row] == player:
            in_row += 1
        else:
            break
    # check left
    for num in range(1, connect_num):
        if col - num >= 0 and board[col - num][row] == player:
            in_row += 1
        else:
            break
    if in_row >= connect_num:
        return True
        
    # check vertical
    in_row = 1
    # check down
    for num in range(1, connect_num):
        if row + num < y_dimension and board[col][row + num] == player:
            in_row += 1
        else:
            break
    if in_row >= connect_num:
        return True
    
    # check diagonal (top-left to bottom-right)
    in_row = 1
    # check top-left
    for num in range(1, connect_num):
        if col - num >= 0 and row - num >= 0 and board[col - num][row - num] == player:
            in_row += 1
        else:
            break
    # check bottom-right
    for num in range(1, connect_num):
        if col + num < x_dimension and row + num < y_dimension and board[col + num][row + num] == player:
            in_row += 1
        else:
            break
    if in_row >= connect_num:
        return True
    
    # check diagonal (top-right to bottom-left)
    in_row = 1
    # check top-right
    for num in range(1, connect_num):
        if col + num < x_dimension and row - num >= 0 and board[col + num][row - num] == player:
            in_row += 1
        else:
            break
    # check bottom-left
    for num in range(1, connect_num):
        if col - num >= 0 and row + num < y_dimension and board[col - num][row + num] == player:
            in_row += 1
        else:
            break
    if in_row >= connect_num:
        return True
    
    return False

def evaluate_board(board, player):
    score = 0
    x_dimension = len(board)
    y_dimension = len(board[0])
    connect_num = 4  # Standard Connect 4
    
    for row in range(y_dimension):
        for col in range(x_dimension - connect_num + 1):
            window = [board[col + i][row] for i in range(connect_num)]
            score += evaluate_window(window, player)
    
    for col in range(x_dimension):
        for row in range(y_dimension - connect_num + 1):
            window = [board[col][row + i] for i in range(connect_num)]
            score += evaluate_window(window, player)
    
    for row in range(y_dimension - connect_num + 1):
        for col in range(x_dimension - connect_num + 1):
            window = [board[col + i][row + i] for i in range(connect_num)]
            score += evaluate_window(window, player)
    
    for row in range(y_dimension - connect_num + 1):
        for col in range(connect_num - 1, x_dimension):
            window = [board[col - i][row + i] for i in range(connect_num)]
            score += evaluate_window(window, player)
    
    center_col = x_dimension // 2
    center_array = [board[center_col][row] for row in range(y_dimension)]
    center_count = center_array.count(player)
    score += center_count * 3
    
    return score

# def evaluate_window(window, player):
#     """
#     Evaluates a window of 4 pieces and returns a score
#     """
#     opponent = 1 if player == 2 else 2
#     
#     if window.count(player) == 4:
#         return 100  # Player wins
#     elif window.count(player) == 3 and window.count(0) == 1:
#         return 5  # Player has 3 in a row with an open spot
#     elif window.count(player) == 2 and window.count(0) == 2:
#         return 2  # Player has 2 in a row with 2 open spots
#     elif window.count(opponent) == 3 and window.count(0) == 1:
#         return -4  # Opponent has 3 in a row with an open spot - block them!
#     else:
#         return 0
def evaluate_window(window, player):
    opponent = 1 if player == 2 else 2
    if window.count(player) == 4:
        return 10000
    elif window.count(player) == 3 and window.count(0) == 1:
        return 100
    elif window.count(player) == 2 and window.count(0) == 2:
        return 10
    elif window.count(player) == 1 and window.count(0) == 3:
        return 1
    elif window.count(opponent) == 3 and window.count(0) == 1:
        return -80  # Increase penalty
    elif window.count(opponent) == 2 and window.count(0) == 2:
        return -10
    else:
        return 0


