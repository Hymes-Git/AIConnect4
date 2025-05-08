import random
import math

class Node:
    def __init__(self, board, parent=None, available_moves=None, current_player=None, top_row=None):
        self.board = board
        self.parent = parent
        self.children = []
        self.visits = 0
        self.wins = 0
        self.untried_moves = available_moves if available_moves is not None else self.get_available_moves(board)
        self.player = current_player
        self.top_row = top_row

    def get_available_moves(self, board):
        # Finds all available columns where a move can be made
        available_moves = []
        for col in range(len(board)):
            if board[col][0] == 0:  # If the column has an empty slot
                available_moves.append(col)
        return available_moves

    def is_fully_expanded(self):
        # Checks if the node has no more untried moves
        return len(self.untried_moves) == 0

    def select_child(self):
        # Selects the child node with the highest win-to-visit ratio using UCT
        best_score = -float('inf')
        best_child = None
        for child in self.children:
            uct_score = child.wins / (child.visits + 1) + math.sqrt(math.log(self.visits + 1) / (child.visits + 1))
            if uct_score > best_score:
                best_score = uct_score
                best_child = child
        return best_child

    def expand(self):
        # Expands the current node by making a move from its untried moves
        move = self.untried_moves.pop()
        new_board = [row[:] for row in self.board]  # Make a copy of the board
        self.make_move(new_board, move, self.player)

        child_node = Node(new_board, parent=self, available_moves=self.get_available_moves(new_board), current_player=3 - self.player, top_row=self.top_row)
        self.children.append(child_node)
        return child_node

    def make_move(self, board, column, player):
        # Make a move on the board
        row = self.top_row[column]
        board[column][row] = player
        self.top_row[column] -= 1

    def backpropagate(self, result):
        # Backpropagates the result of the simulation up the tree
        self.visits += 1
        self.wins += result
        if self.parent:
            self.parent.backpropagate(result)

class MCTS:
    def __init__(self, board, top_row, available_moves, current_player, simulations=100):
        self.board = board
        self.top_row = top_row
        self.available_moves = available_moves
        self.current_player = current_player
        self.simulations = simulations
        self.root = Node(board, available_moves=available_moves, current_player=current_player, top_row=top_row)

    def simulate(self, node):
        # Simulates the game until completion using random moves
        current_board = [row[:] for row in node.board]  # Copy of the board
        current_top_row = node.top_row[:]
        current_player = node.player

        available_moves = node.get_available_moves(current_board)

        while available_moves:
            move = random.choice(available_moves)
            node.make_move(current_board, move, current_player)
            available_moves.remove(move)
            current_player = 3 - current_player  # Switch player (1 -> 2 or 2 -> 1)

        return self.evaluate_board(current_board)

    def evaluate_board(self, board):
        # Evaluates the board to decide the result (1 for player 1 win, -1 for player 2 win, 0 for draw)
        # You can expand this with more complex evaluation, but for simplicity, we're using a random outcome here.
        return random.choice([1, -1, 0])

    def run(self):
        # Perform MCTS simulations
        for _ in range(self.simulations):
            node = self.root
            while not node.is_fully_expanded():  # Expand the tree until a fully expanded node is found
                node = node.select_child()  # Select the best child

            if not node.is_fully_expanded():
                node = node.expand()  # Expand the node by adding a new child

            result = self.simulate(node)  # Simulate the outcome from this node
            node.backpropagate(result)  # Backpropagate the result up the tree

        return self.select_best_move()

    def select_best_move(self):
        # Select the best move based on the highest win ratio
        best_child = self.root.select_child()
        if best_child:
            available_moves = best_child.untried_moves if best_child.untried_moves else best_child.get_available_moves(best_child.board)
            if available_moves:  # Always ensure there's at least one available move
                return random.choice(available_moves)
        
        # Fallback: If no child nodes were selected, return a random move from the root node
        return random.choice(self.root.get_available_moves(self.board))

    def mcts_move(self):
        # Returns the best move after running the MCTS simulations
        return self.run()
