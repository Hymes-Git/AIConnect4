# import random
#
# class MCTS:
#     def __init__(self, board, top_row, available_moves, current_player, depth=4):
#         self.board = board
#         self.top_row = top_row
#         self.available_moves = available_moves
#         self.current_player = current_player
#         self.depth = depth
#         self.simulations = 100  
#
#     def mcts_move(self):
#         root_node = Node(self.board, self.top_row, self.available_moves, self.current_player)
#         
#         for _ in range(self.simulations):
#             node = self.selection(root_node)
#             if not node.is_terminal():
#                 node = self.expansion(node)
#             winner = self.simulation(node)
#             self.backpropagation(node, winner)
#
#         best_move = self.best_move(root_node)
#         return best_move
#
#     def selection(self, node):
#         while node.children:
#                         node = max(node.children, key=lambda child: child.uct_value())
#         return node
#
#     def expansion(self, node):
#         possible_moves = node.get_possible_moves()
#         for move in possible_moves:
#             child_board, child_top_row, child_available_moves = node.apply_move(move)
#             child_node = Node(child_board, child_top_row, child_available_moves, 3 - node.player)  
#             node.children.append(child_node)
#         return random.choice(node.children)
#
#     def simulation(self, node):
#         board_copy = [row.copy() for row in node.board]
#         top_row_copy = node.top_row[:]
#         available_moves_copy = node.available_moves[:]
#         current_player = node.player
#         while True:
#             if not available_moves_copy:
#                 break
#             move = random.choice(available_moves_copy)
#             available_moves_copy.remove(move)
#             top_row_copy[move] -= 1
#             board_copy[move][top_row_copy[move]] = current_player
#             current_player = 3 - current_player  
#         return self.check_winner(board_copy)
#
#     def backpropagation(self, node, winner):
#         while node:
#             node.visits += 1
#             if node.player == winner:
#                 node.wins += 1
#             node = node.parent
#
#     def best_move(self, node):
#         return max(node.children, key=lambda child: child.visits).move
#
#     def check_winner(self, board):
#         for x in range(7):
#             for y in range(6):
#                 if board[x][y] == 0:
#                     continue
#                 player = board[x][y]
#                 
#                 if x + 3 < 7 and all(board[x+i][y] == player for i in range(4)):
#                     return player
#                 
#                 if y + 3 < 6 and all(board[x][y+i] == player for i in range(4)):
#                     return player
#                 
#                 if x + 3 < 7 and y + 3 < 6 and all(board[x+i][y+i] == player for i in range(4)):
#                     return player
#                 
#                 if x - 3 >= 0 and y + 3 < 6 and all(board[x-i][y+i] == player for i in range(4)):
#                     return player
#         return 0  
#
# class Node:
#     def __init__(self, board, top_row, available_moves, player, parent=None, move=None):
#         self.board = board
#         self.top_row = top_row
#         self.available_moves = available_moves
#         self.player = player
#         self.parent = parent
#         self.move = move
#         self.visits = 0
#         self.wins = 0
#         self.children = []
#
#     def is_terminal(self):
#         return self.get_possible_moves() == []
#
#     def get_possible_moves(self):
#         return [move for move in self.available_moves if self.top_row[move] >= 0]
#
#     def apply_move(self, move):
#         new_board = [row.copy() for row in self.board]
#         new_top_row = self.top_row[:]
#         new_available_moves = self.available_moves[:]
#         
#         new_top_row[move] -= 1
#         new_board[move][new_top_row[move]] = self.player
#         if new_top_row[move] < 0:
#             new_available_moves.remove(move)
#         return new_board, new_top_row, new_available_moves
#
#     def uct_value(self, exploration_weight=1.0):
#         if self.visits == 0:
#             return float('inf')
#         return (self.wins / self.visits) + exploration_weight * (2 * (self.parent.visits)**0.5) / (self.visits)
#
import random
import math

class Node:
    def __init__(self, board, parent=None, available_moves=None, current_player=None):
        self.board = board
        self.parent = parent
        self.children = []
        self.visits = 0
        self.wins = 0
        self.untried_moves = available_moves if available_moves is not None else self.get_available_moves(board)
        self.player = current_player
        self.player_to_move = current_player
    
    def get_available_moves(self, board):
        # Function to find available moves in the current board state
        available_moves = []
        for col in range(len(board)):
            if board[col][0] == 0:  # If the column has available space
                available_moves.append(col)
        return available_moves
    
    def is_fully_expanded(self):
        return len(self.untried_moves) == 0

    def best_child(self, exploration_weight=1.0):
        best_score = -float('inf')
        best_node = None
        for child in self.children:
            score = child.wins / (child.visits + 1) + exploration_weight * math.sqrt(math.log(self.visits + 1) / (child.visits + 1))
            if score > best_score:
                best_score = score
                best_node = child
        return best_node

    def select_child(self):
        # Selects the best child based on exploration/exploitation balance
        return self.best_child()

class MCTS:
    def __init__(self, board, top_row, available_moves, current_player, depth=4, simulations=100):
        self.board = board
        self.top_row = top_row
        self.available_moves = available_moves
        self.current_player = current_player
        self.depth = depth
        self.simulations = simulations

    def simulate(self, node):
        # Simulate the game from the given node (board state) using random moves
        current_board = [row[:] for row in node.board]  # Copy the board
        available_moves = node.untried_moves[:]
        current_player = node.player_to_move
        
        while len(available_moves) > 0:
            move = random.choice(available_moves)
            self.make_move(current_board, move, current_player)
            available_moves.remove(move)
            current_player = 3 - current_player  # Switch player (1->2, 2->1)

        return self.evaluate_board(current_board)  # Evaluate the final board state

    def evaluate_board(self, board):
        # Evaluate the board to decide win/loss for simulation
        # Placeholder for a simple evaluation function
        # Return 1 for win for player 1, -1 for win for player 2, 0 for a draw
        return random.choice([-1, 1, 0])

    def make_move(self, board, move, player):
        # Make the move on the board
        for row in reversed(range(len(board))):
            if board[move][row] == 0:
                board[move][row] = player
                break
    
    def backpropagate(self, node, result):
        # Backpropagate the result from a simulation
        while node is not None:
            node.visits += 1
            node.wins += result
            node = node.parent

    def mcts_move(self):
        root = Node(self.board, available_moves=self.available_moves, current_player=self.current_player)
        
        for _ in range(self.simulations):
            node = root
            while not node.is_fully_expanded():
                node = node.select_child()
            result = self.simulate(node)
            self.backpropagate(node, result)
        
        best_child = root.best_child(0)  # Select the best child without exploration
        if best_child:
            return random.choice(best_child.untried_moves)  # Return a valid move
        else:
            return None  # If no move found, return None (fallback)

