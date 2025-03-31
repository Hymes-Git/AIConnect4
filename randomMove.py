import random
import numpy

def randomMove(board, topRow):
    x_dimension = len(topRow)

    valid = False

    for elem in topRow:
        if elem >= 0:
            valid = True

    if valid == False:
        return -1

    while True:
        column = random.randint(0, x_dimension-1)
        if topRow[column] >= 0:
            return column

