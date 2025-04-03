import random
import numpy

def randomMove(board, topRow, availableMoves, player):
    if len(availableMoves) == 0:
        return -1 

    return random.choice(availableMoves)


