import random

class MCTS:
    def __init__(self, board, top_row, available_moves, current_player, depth=4):
        self.board = board
        self.top_row = top_row
        self.available_moves = available_moves
        self.current_player = current_player
        self.depth = depth
        self.simulations = 100  

    def mcts_move(self):
        root_node = Node(self.board, self.top_row, self.available_moves, self.current_player)
        
        for _ in range(self.simulations):
            node = self.selection(root_node)
            if not node.is_terminal():
                node = self.expansion(node)
            winner = self.simulation(node)
            self.backpropagation(node, winner)

        best_move = self.best_move(root_node)
        return best_move

    def selection(self, node):
        while node.children:
                        node = max(node.children, key=lambda child: child.uct_value())
        return node

    def expansion(self, node):
        possible_moves = node.get_possible_moves()
        for move in possible_moves:
            child_board, child_top_row, child_available_moves = node.apply_move(move)
            child_node = Node(child_board, child_top_row, child_available_moves, 3 - node.player)  
            node.children.append(child_node)
        return random.choice(node.children)

    def simulation(self, node):
        board_copy = [row.copy() for row in node.board]
        top_row_copy = node.top_row[:]
        available_moves_copy = node.available_moves[:]
        current_player = node.player
        while True:
            if not available_moves_copy:
                break
            move = random.choice(available_moves_copy)
            available_moves_copy.remove(move)
            top_row_copy[move] -= 1
            board_copy[move][top_row_copy[move]] = current_player
            current_player = 3 - current_player  # Switch player
        return self.check_winner(board_copy)

    def backpropagation(self, node, winner):
        while node:
            node.visits += 1
            if node.player == winner:
                node.wins += 1
            node = node.parent

    def best_move(self, node):
        return max(node.children, key=lambda child: child.visits).move

    def check_winner(self, board):
        for x in range(7):
            for y in range(6):
                if board[x][y] == 0:
                    continue
                player = board[x][y]
                # Check horizontal
                if x + 3 < 7 and all(board[x+i][y] == player for i in range(4)):
                    return player
                # Check vertical
                if y + 3 < 6 and all(board[x][y+i] == player for i in range(4)):
                    return player
                # Check diagonal (left-up to right-down)
                if x + 3 < 7 and y + 3 < 6 and all(board[x+i][y+i] == player for i in range(4)):
                    return player
                # Check diagonal (right-up to left-down)
                if x - 3 >= 0 and y + 3 < 6 and all(board[x-i][y+i] == player for i in range(4)):
                    return player
        return 0  

class Node:
    def __init__(self, board, top_row, available_moves, player, parent=None, move=None):
        self.board = board
        self.top_row = top_row
        self.available_moves = available_moves
        self.player = player
        self.parent = parent
        self.move = move
        self.visits = 0
        self.wins = 0
        self.children = []

    def is_terminal(self):
        return self.get_possible_moves() == []

    def get_possible_moves(self):
        return [move for move in self.available_moves if self.top_row[move] >= 0]

    def apply_move(self, move):
        new_board = [row.copy() for row in self.board]
        new_top_row = self.top_row[:]
        new_available_moves = self.available_moves[:]
        
        new_top_row[move] -= 1
        new_board[move][new_top_row[move]] = self.player
        if new_top_row[move] < 0:
            new_available_moves.remove(move)
        return new_board, new_top_row, new_available_moves

    def uct_value(self, exploration_weight=1.0):
        if self.visits == 0:
            return float('inf')
        return (self.wins / self.visits) + exploration_weight * (2 * (self.parent.visits)**0.5) / (self.visits)

