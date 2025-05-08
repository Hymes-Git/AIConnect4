import math

class Node:
    def __init__(self, board, parent=None, available_moves=None, current_player=None, top_row=None):
        self.board = board
        self.parent = parent
        self.children = []
        self.visits = 0
        self.wins = 0
        
        # Initialize top_row properly - if it's None, create it based on the board
        if top_row is None:
            # Calculate the top row based on the board state
            self.top_row = self.calculate_top_row(board)
        else:
            # Make a copy of the provided top_row
            self.top_row = top_row[:]
            
        # Set current player, defaulting to 1 if not specified
        self.player = current_player if current_player is not None else 1
        
        # Always make sure this is a list, never None
        self.untried_moves = available_moves if available_moves is not None else self.get_available_moves(board)
    
    def calculate_top_row(self, board):
        """Calculate the top row (first empty cell) for each column"""
        top_row = []
        for col in range(len(board)):
            # Find the first empty cell (value 0) from bottom to top
            row = len(board[col]) - 1
            while row >= 0 and board[col][row] != 0:
                row -= 1
            top_row.append(row)
        return top_row
    
    def get_available_moves(self, board):
        moves = []
        for col in range(len(board)):
            # Check if the column has any empty spaces
            if any(cell == 0 for cell in board[col]):
                moves.append(col)
        return moves
    
    def is_fully_expanded(self):
        return len(self.untried_moves) == 0
    
    def select_child(self):
        if not self.children:
            return self  # Return self if no children available
        
        best_score = -float("inf")
        best_child = None
        for child in self.children:
            if child.visits == 0:
                score = float("inf")
            else:
                score = child.wins / child.visits + math.sqrt(2 * math.log(self.visits + 1) / child.visits)
            if score > best_score:
                best_score = score
                best_child = child
                
        return best_child  # This should never be None if children exist
    
    def expand(self):
        if not self.untried_moves:
            return self  # Already fully expanded
            
        move = self.untried_moves.pop()
        
        # Copy board and top_row safely
        new_board = [col[:] for col in self.board]
        new_top_row = self.top_row[:]
        
        # Make the move
        row = new_top_row[move]
        if row < 0:
            # Handle column overflow - try another move if possible
            if self.untried_moves:
                return self.expand()
            return self
            
        new_board[move][row] = self.player
        new_top_row[move] -= 1
        
        # Create new child node with opponent as current player
        child = Node(
            new_board, 
            parent=self, 
            available_moves=self.get_available_moves(new_board),
            current_player=3 - self.player,  # Switch player (assuming players are 1 and 2)
            top_row=new_top_row
        )
        
        self.children.append(child)
        return child
    
    def backpropagate(self, result):
        self.visits += 1
        self.wins += result
        if self.parent:
            self.parent.backpropagate(1 - result)  # Invert result for opponent

# Example MCTS search function
def mcts_search(root_state, iterations=1000):
    # Create root node
    root = Node(board=root_state, current_player=1)
    
    for _ in range(iterations):
        # Selection
        node = root
        while node.is_fully_expanded() and node.children:
            node = node.select_child()
        
        # Expansion
        if not node.is_fully_expanded() and node.untried_moves:
            node = node.expand()
        
        # Simulation - simplified random playout
        result = simulate_random_game(node.board, node.player)
        
        # Backpropagation
        node.backpropagate(result)
    
    # Return best move
    best_child = None
    most_visits = -1
    for child in root.children:
        if child.visits > most_visits:
            most_visits = child.visits
            best_child = child
    
    # Find the move that led to the best child
    for col in range(len(root_state)):
        # Check if this move leads to the best child's board
        if best_child and any(child.board[col] != root_state[col] for child in [best_child]):
            return col
    
    # Fallback: return first available move
    for col in range(len(root_state)):
        if root_state[col][0] == 0:
            return col
    
    return None  # No valid moves

def simulate_random_game(board, player):
    """Simulate a random game and return the result."""
    # This is a placeholder - implement actual game simulation
    # For now, just return a random result
    import random
    return random.random() > 0.5
