# import math
# import random
# import time
# import numpy as np
#
# class Node:
#     def __init__(self, board, parent=None, available_moves=None, current_player=None, top_row=None):
#         self.board = [col[:] for col in board]  # Deep copy
#         self.parent = parent
#         self.children = []
#         self.visits = 0
#         self.wins = 0
#         
#         # Initialize top_row properly
#         if top_row is None:
#             # Calculate top row based on board
#             self.top_row = []
#             for col in range(len(board)):
#                 for row in range(len(board[col])):
#                     if board[col][row] == 0:
#                         self.top_row.append(row)
#                         break
#                 else:
#                     self.top_row.append(-1)  # Column is full
#         else:
#             self.top_row = top_row[:]
#         
#         # Set current player
#         self.player = current_player
#         
#         # Make sure available_moves is a list
#         if available_moves is None:
#             self.untried_moves = []
#             for col in range(len(board)):
#                 if self.top_row[col] >= 0:
#                     self.untried_moves.append(col)
#         else:
#             self.untried_moves = available_moves[:]
#     
#     def is_fully_expanded(self):
#         return len(self.untried_moves) == 0
#     
#     def select_child(self):
#         if not self.children:
#             return self
#         
#         # UCB1 formula for selection
#         c = 1.41  # Exploration parameter
#         best_score = -float("inf")
#         best_child = self.children[0] if self.children else self
#         
#         for child in self.children:
#             if child.visits == 0:
#                 score = float("inf")
#             else:
#                 # UCB1 formula: wins/visits + c * sqrt(ln(parent_visits) / visits)
#                 score = child.wins / child.visits + c * math.sqrt(2 * math.log(self.visits) / child.visits)
#             
#             if score > best_score:
#                 best_score = score
#                 best_child = child
#         
#         return best_child
#     
#     def expand(self):
#         if not self.untried_moves:
#             return self
#         
#         try:
#             # Pick a random move from untried moves
#             move = random.choice(self.untried_moves)
#             self.untried_moves.remove(move)
#             
#             # Make a deep copy of the board and top row
#             new_board = [col[:] for col in self.board]
#             new_top_row = self.top_row[:]
#             
#             # Execute move
#             row = new_top_row[move]
#             if row < 0:
#                 # Invalid move (column is full)
#                 return self
#             
#             # Place piece
#             new_board[move][row] = self.player
#             new_top_row[move] -= 1
#             
#             # Calculate new available moves
#             new_available = []
#             for col in range(len(new_board)):
#                 if new_top_row[col] >= 0:
#                     new_available.append(col)
#             
#             # Create child with opponent as current player
#             next_player = 3 - self.player  # Switch between player 1 and 2
#             child = Node(
#                 board=new_board,
#                 parent=self,
#                 available_moves=new_available,
#                 current_player=next_player,
#                 top_row=new_top_row
#             )
#             
#             self.children.append(child)
#             return child
#             
#         except Exception as e:
#             print(f"Error in expand: {e}")
#             return self
#     
#     def backpropagate(self, result):
#         self.visits += 1
#         
#         # For player 1, we want to maximize their win probability
#         # For player 2, we want to minimize player 1's win probability (or maximize player 2's)
#         if self.player == 1:
#             self.wins += result
#         else:
#             self.wins += (1 - result)
#             
#         if self.parent:
#             self.parent.backpropagate(result)
#
# def check_win(board, move_x, move_y, player, connect_num=4):
#     """Check if the last move resulted in a win"""
#     x_dimension = len(board)
#     y_dimension = len(board[0])
#     
#     # Check horizontal
#     in_row = 1
#     for num in range(1, connect_num):
#         if move_x + num < x_dimension and board[move_x + num][move_y] == player:
#             in_row += 1
#         else:
#             break
#     
#     for num in range(1, connect_num):
#         if move_x - num >= 0 and board[move_x - num][move_y] == player:
#             in_row += 1
#         else:
#             break
#     
#     if in_row >= connect_num:
#         return True
#     
#     # Check vertical
#     in_row = 1
#     for num in range(1, connect_num):
#         if move_y + num < y_dimension and board[move_x][move_y + num] == player:
#             in_row += 1
#         else:
#             break
#     
#     if in_row >= connect_num:
#         return True
#     
#     # Check diagonal (top-left to bottom-right)
#     in_row = 1
#     for num in range(1, connect_num):
#         if move_x - num >= 0 and move_y - num >= 0 and board[move_x - num][move_y - num] == player:
#             in_row += 1
#         else:
#             break
#     
#     for num in range(1, connect_num):
#         if move_x + num < x_dimension and move_y + num < y_dimension and board[move_x + num][move_y + num] == player:
#             in_row += 1
#         else:
#             break
#     
#     if in_row >= connect_num:
#         return True
#     
#     # Check diagonal (top-right to bottom-left)
#     in_row = 1
#     for num in range(1, connect_num):
#         if move_x + num < x_dimension and move_y - num >= 0 and board[move_x + num][move_y - num] == player:
#             in_row += 1
#         else:
#             break
#     
#     for num in range(1, connect_num):
#         if move_x - num >= 0 and move_y + num < y_dimension and board[move_x - num][move_y + num] == player:
#             in_row += 1
#         else:
#             break
#     
#     if in_row >= connect_num:
#         return True
#     
#     return False
#
# def simulate_game(board, top_row, player, connect_num=4):
#     """Simulate a random game from the current position"""
#     # Make deep copies to avoid modifying originals
#     sim_board = [col[:] for col in board]
#     sim_top_row = top_row[:]
#     current_player = player
#     
#     # Get valid moves
#     valid_moves = []
#     for col in range(len(sim_board)):
#         if sim_top_row[col] >= 0:
#             valid_moves.append(col)
#     
#     last_move_x, last_move_y = -1, -1
#     
#     # Play until game over
#     while valid_moves:
#         # Random move
#         move = random.choice(valid_moves)
#         row = sim_top_row[move]
#         
#         # Place piece
#         sim_board[move][row] = current_player
#         last_move_x, last_move_y = move, row
#         sim_top_row[move] -= 1
#         
#         # Check for win
#         if check_win(sim_board, last_move_x, last_move_y, current_player, connect_num):
#             # Return 1 if player 1 wins, 0 if player 2 wins
#             return 1 if current_player == 1 else 0
#         
#         # Update valid moves
#         if sim_top_row[move] < 0 and move in valid_moves:
#             valid_moves.remove(move)
#         
#         # Switch player
#         current_player = 3 - current_player
#     
#     # Draw
#     return 0.5
#
# def mcts_move(board, top_row, available_moves, current_player, iterations=1000, time_limit=None):
#     """Get best move using MCTS algorithm"""
#     start_time = time.time()
#     
#     # Create root node
#     root = Node(board, current_player=current_player, top_row=top_row, available_moves=available_moves)
#     
#     # Run MCTS iterations
#     iteration = 0
#     while iteration < iterations:
#         if time_limit and (time.time() - start_time > time_limit):
#             break
#         
#         # Selection phase - traverse tree until we reach a leaf node
#         node = root
#         while node.is_fully_expanded() and node.children:
#             node = node.select_child()
#         
#         # If we can expand this node, do so
#         if not node.is_fully_expanded() and node.untried_moves:
#             node = node.expand()
#         
#         # Simulation phase - play out a random game from this position
#         if node != root:  # Only simulate if we've moved at least one step
#             result = simulate_game(node.board, node.top_row, node.player)
#             
#             # Backpropagation phase - update statistics up the tree
#             node.backpropagate(result)
#         else:
#             # If we couldn't move from root, try again
#             continue
#             
#         iteration += 1
#     
#     # Choose the best child based on most visits
#     if not root.children:
#         # If no children, choose a random move
#         return random.choice(available_moves) if available_moves else -1
#         
#     # Find child with highest visit count
#     best_child = max(root.children, key=lambda c: c.visits)
#     
#     # Determine which move led to this child
#     for col in range(len(board)):
#         for row in range(len(board[col])):
#             if root.board[col][row] != best_child.board[col][row]:
#                 return col
#     
#     # Fallback - return first available move
#     return available_moves[0] if available_moves else -1
import math
import random
import time
import numpy as np

class Node:
    def __init__(self, board, parent=None, available_moves=None, current_player=None, top_row=None):
        self.board = [col[:] for col in board]  # Deep copy
        self.parent = parent
        self.children = []
        self.visits = 0
        self.wins = 0
        
        # Initialize top_row properly
        if top_row is None:
            # Calculate top row based on board
            self.top_row = []
            for col in range(len(board)):
                for row in range(len(board[col])):
                    if board[col][row] == 0:
                        self.top_row.append(row)
                        break
                else:
                    self.top_row.append(-1)  # Column is full
        else:
            self.top_row = top_row[:]
        
        # Set current player
        self.player = current_player
        
        # Make sure available_moves is a list
        if available_moves is None:
            self.untried_moves = []
            for col in range(len(board)):
                if self.top_row[col] >= 0:
                    self.untried_moves.append(col)
        else:
            self.untried_moves = available_moves[:]
    
    def is_fully_expanded(self):
        return len(self.untried_moves) == 0
    
    def select_child(self):
        if not self.children:
            return self
        
        # UCB1 formula for selection
        c = 1.41  # Exploration parameter
        best_score = -float("inf")
        best_child = self.children[0] if self.children else self
        
        for child in self.children:
            if child.visits == 0:
                score = float("inf")
            else:
                # UCB1 formula: wins/visits + c * sqrt(ln(parent_visits) / visits)
                score = child.wins / child.visits + c * math.sqrt(2 * math.log(self.visits) / child.visits)
            
            if score > best_score:
                best_score = score
                best_child = child
        
        return best_child
    
    def expand(self):
        if not self.untried_moves:
            return self
        
        try:
            # Pick a random move from untried moves
            move = random.choice(self.untried_moves)
            self.untried_moves.remove(move)
            
            # Make a deep copy of the board and top row
            new_board = [col[:] for col in self.board]
            new_top_row = self.top_row[:]
            
            # Execute move
            row = new_top_row[move]
            if row < 0:
                # Invalid move (column is full)
                return self
            
            # Place piece
            new_board[move][row] = self.player
            new_top_row[move] -= 1
            
            # Calculate new available moves
            new_available = []
            for col in range(len(new_board)):
                if new_top_row[col] >= 0:
                    new_available.append(col)
            
            # Create child with opponent as current player
            next_player = 3 - self.player  # Switch between player 1 and 2
            child = Node(
                board=new_board,
                parent=self,
                available_moves=new_available,
                current_player=next_player,
                top_row=new_top_row
            )
            
            self.children.append(child)
            return child
            
        except Exception as e:
            print(f"Error in expand: {e}")
            return self
    
    def backpropagate(self, result):
        self.visits += 1
        
        # For player 1, we want to maximize their win probability
        # For player 2, we want to minimize player 1's win probability (or maximize player 2's)
        if self.player == 1:
            self.wins += result
        else:
            self.wins += (1 - result)
            
        if self.parent:
            self.parent.backpropagate(result)

def check_win(board, move_x, move_y, player, connect_num=4):
    """Check if the last move resulted in a win"""
    x_dimension = len(board)
    y_dimension = len(board[0])
    
    # Check horizontal
    in_row = 1
    for num in range(1, connect_num):
        if move_x + num < x_dimension and board[move_x + num][move_y] == player:
            in_row += 1
        else:
            break
    
    for num in range(1, connect_num):
        if move_x - num >= 0 and board[move_x - num][move_y] == player:
            in_row += 1
        else:
            break
    
    if in_row >= connect_num:
        return True
    
    # Check vertical
    in_row = 1
    for num in range(1, connect_num):
        if move_y + num < y_dimension and board[move_x][move_y + num] == player:
            in_row += 1
        else:
            break
    
    if in_row >= connect_num:
        return True
    
    # Check diagonal (top-left to bottom-right)
    in_row = 1
    for num in range(1, connect_num):
        if move_x - num >= 0 and move_y - num >= 0 and board[move_x - num][move_y - num] == player:
            in_row += 1
        else:
            break
    
    for num in range(1, connect_num):
        if move_x + num < x_dimension and move_y + num < y_dimension and board[move_x + num][move_y + num] == player:
            in_row += 1
        else:
            break
    
    if in_row >= connect_num:
        return True
    
    # Check diagonal (top-right to bottom-left)
    in_row = 1
    for num in range(1, connect_num):
        if move_x + num < x_dimension and move_y - num >= 0 and board[move_x + num][move_y - num] == player:
            in_row += 1
        else:
            break
    
    for num in range(1, connect_num):
        if move_x - num >= 0 and move_y + num < y_dimension and board[move_x - num][move_y + num] == player:
            in_row += 1
        else:
            break
    
    if in_row >= connect_num:
        return True
    
    return False

def find_winning_or_blocking_move(sim_board, sim_top_row, player):
    """Find a winning move for the player or a move that blocks opponent win"""
    opponent = 3 - player
    
    # First check for winning move
    for col in range(len(sim_board)):
        if sim_top_row[col] >= 0:
            row = sim_top_row[col]
            # Try move
            sim_board[col][row] = player
            # Check win
            if check_win(sim_board, col, row, player):
                # Undo move
                sim_board[col][row] = 0
                return col
            # Undo move
            sim_board[col][row] = 0
    
    # Then check for blocking opponent's win
    for col in range(len(sim_board)):
        if sim_top_row[col] >= 0:
            row = sim_top_row[col]
            # Try opponent move
            sim_board[col][row] = opponent
            # Check if opponent would win
            if check_win(sim_board, col, row, opponent):
                # Undo move
                sim_board[col][row] = 0
                return col
            # Undo move
            sim_board[col][row] = 0
    
    return None  # No winning or blocking move found

def simulate_game(board, top_row, player, connect_num=4):
    """Simulate a game from the current position with smart play"""
    # Make deep copies to avoid modifying originals
    sim_board = [col[:] for col in board]
    sim_top_row = top_row[:]
    current_player = player
    
    # Get valid moves
    valid_moves = []
    for col in range(len(sim_board)):
        if sim_top_row[col] >= 0:
            valid_moves.append(col)
    
    last_move_x, last_move_y = -1, -1
    
    # Play until game over
    while valid_moves:
        # Check for winning or blocking moves first
        smart_move = find_winning_or_blocking_move(sim_board, sim_top_row, current_player)
        
        if smart_move is not None and smart_move in valid_moves:
            move = smart_move
        else:
            # If no smart move, pick random but favor center columns
            center_weight = []
            center = len(sim_board) // 2
            for m in valid_moves:
                # Give higher weight to center columns
                weight = 5 - min(abs(m - center), 3)  # Columns closer to center get higher weight
                center_weight.extend([m] * weight)
            move = random.choice(center_weight if center_weight else valid_moves)
        
        row = sim_top_row[move]
        
        # Place piece
        sim_board[move][row] = current_player
        last_move_x, last_move_y = move, row
        sim_top_row[move] -= 1
        
        # Check for win
        if check_win(sim_board, last_move_x, last_move_y, current_player, connect_num):
            # Return 1 if player 1 wins, 0 if player 2 wins
            return 1 if current_player == 1 else 0
        
        # Update valid moves
        if sim_top_row[move] < 0 and move in valid_moves:
            valid_moves.remove(move)
        
        # Switch player
        current_player = 3 - current_player
    
    # Draw
    return 0.5

def find_winning_move(board, top_row, player, connect_num=4):
    """Check if player has a winning move and return it"""
    for col in range(len(board)):
        if top_row[col] >= 0:  # If column is not full
            row = top_row[col]
            
            # Make the move
            board[col][row] = player
            
            # Check if this move wins
            if check_win(board, col, row, player, connect_num):
                # Undo move and return the winning column
                board[col][row] = 0
                return col
            
            # Undo move
            board[col][row] = 0
    
    return None

def mcts_move(board, top_row, available_moves, current_player, iterations=1000, time_limit=None):
    """Get best move using MCTS algorithm with added winning move detection"""
    if not available_moves:
        return -1
        
    # Make copies to avoid modifying originals
    board_copy = [col[:] for col in board]
    top_row_copy = top_row[:]
    
    # 1. First check if we can win in one move
    winning_move = find_winning_move(board_copy, top_row_copy, current_player)
    if winning_move is not None:
        print(f"Player {current_player} found winning move: {winning_move}")
        return winning_move
        
    # 2. Then check if we need to block opponent's winning move
    opponent = 3 - current_player
    blocking_move = find_winning_move(board_copy, top_row_copy, opponent)
    if blocking_move is not None:
        print(f"Player {current_player} blocking opponent's winning move: {blocking_move}")
        return blocking_move
    
    # 3. If no immediate wins/blocks, use MCTS
    start_time = time.time()
    
    # Create root node
    root = Node(board, current_player=current_player, top_row=top_row, available_moves=available_moves)
    
    # Run MCTS iterations
    iteration = 0
    while iteration < iterations:
        if time_limit and (time.time() - start_time > time_limit):
            break
        
        # Selection phase - traverse tree until we reach a leaf node
        node = root
        while node.is_fully_expanded() and node.children:
            node = node.select_child()
        
        # If we can expand this node, do so
        if not node.is_fully_expanded() and node.untried_moves:
            node = node.expand()
        
        # Simulation phase - play out a random game from this position
        if node != root:  # Only simulate if we've moved at least one step
            result = simulate_game(node.board, node.top_row, node.player)
            
            # Backpropagation phase - update statistics up the tree
            node.backpropagate(result)
        else:
            # If we couldn't move from root, try again
            continue
            
        iteration += 1
    
    # Choose the best child based on most visits
    if not root.children:
        # If no children, choose a random move
        return random.choice(available_moves)
        
    # Find child with highest visit count
    best_child = max(root.children, key=lambda c: c.visits)
    
    # Determine which move led to this child
    for col in range(len(board)):
        for row in range(len(board[0])):
            if col < len(board) and row < len(board[0]) and row == top_row[col]:
                if root.board[col][row] == 0 and best_child.board[col][row] != 0:
                    return col
    
    # Fallback - get center-biased random move
    center = len(board) // 2
    sorted_moves = sorted(available_moves, key=lambda x: abs(x - center))
    return sorted_moves[0] if sorted_moves else -1
