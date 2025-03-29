# this script was written assuming python=3.9
import numpy as np
# import sys
import argparse
import random


# creates a 6 row 7 coloumn matrix where all elements are init to value of 0
def create_board():
    return np.zeros((6, 7), dtype=int)

# to see the board the way we would expect to see it as humans we need to print in reverse order
# np.flip(matrix,axis) if axis==0 flip rows. if axis == 1 flip coloumns
def print_board(board):
    board = np.flip(board, 0)

    # Define ANSI color codes for background colors
    colors = {0: "\033[47m  \033[0m", 1: "\033[44m  \033[0m", 2: "\033[41m  \033[0m"}  # White, Blue, Red

    # Print the array with colors, spaces between squares, and reduced spacing between rows
    for row in board:
        for element in row:
            print(f"{colors[element]} ", end="")  # Add an extra space for spacing
        print()  # Move to the next row
        print()  # Add space between rows


# check to see if top space in coloumn is empty
def is_valid_move(board, col):
    return board[5][col] == 0

# iterate through every element in the coloumn from the lowest level to the highest and return boolean about ability for player to take ownership of element in coloumn
def drop_piece(board, col, player):
    for row in range(6):
        if board[row][col] == 0:
            board[row][col] = player
            return True
    return False


def is_game_over(board):
    # Check horizontal
    for row in range(6):
        for col in range(4):
            if board[row][col] != 0 and all(board[row][col + i] == board[row][col] for i in range(4)):
                return True
    
    # Check vertical
    for row in range(3):
        for col in range(7):
            if board[row][col] != 0 and all(board[row + i][col] == board[row][col] for i in range(4)):
                return True
    
    # Check diagonal (positive slope)
    for row in range(3):
        for col in range(4):
            if board[row][col] != 0 and all(board[row + i][col + i] == board[row][col] for i in range(4)):
                return True
    
    # Check diagonal (negative slope)
    for row in range(3, 6):
        for col in range(4):
            if board[row][col] != 0 and all(board[row - i][col + i] == board[row][col] for i in range(4)):
                return True

    return False

def random_bot_move(board):
    while True:
        col = random.randint(0, 6)
        if is_valid_move(board, col):
            return col

def main():
    parser = argparse.ArgumentParser(description="Play Connect Four")
    parser.add_argument("--bot_count", type=int, choices=[0, 1, 2], default=1, help="Number of bots in the game (0, 1, or 2)")
    args = parser.parse_args()

    bot_count = args.bot_count # number of ai bots in the game 
    board = create_board()
    game_over = False
    player = 1 #flag to determine player turn. if we have 1 bot player==1 will be the human

    while not game_over:
        print_board(board)
        # col = int(input(f"Player {player}, choose a column (0-6): "))
        if bot_count == 2 or (bot_count == 1 and player == 2):
            col = random_bot_move(board)
            print(f"Bot Player {player} chooses column {col}")
        else:
            col = int(input(f"Player {player}, choose a column (0-6): "))
        
        if 0 <= col < 7:
            if is_valid_move(board, col):
                drop_piece(board, col, player)
                if is_game_over(board):
                    print_board(board)
                    print(f"Player {player} wins!")
                    game_over = True
                else:
                    player = 3 - player  # alternate between player 1 and 2


# this section of code should be unreachable for bots
            else:
                print("Column is full. Choose another one.")
        else: 
            print("Invalid column. Choose between 0 and 6.")



if __name__ == "__main__":
    main()
