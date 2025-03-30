from tkinter import *
import argparse
import numpy as np

class GUI:
    def __init__(self):
        self.x_dimension = 7
        self. y_dimension = 6
        self.root=Tk()
        self.connectNum = 4

        self.gameMode = 0 # gameMode determines human v. human, human v. AI or AI v. AI

        self.root.title("Connect 4")

        # adjust the height and width of the window
        windowWidth = 1280
        windowHeight = 720
        screenWidth = self.root.winfo_screenwidth()
        screenHeight = self.root.winfo_screenheight()
        centerX = int(screenWidth/2 - windowWidth / 2)
        centerY = int(screenHeight/2 - windowHeight / 2)
        self.root.minsize(int(screenWidth / 4), int(screenHeight / 4))  # width, height
        self.root.maxsize(screenWidth,screenHeight)
        self.root.geometry(f'{windowWidth}x{windowHeight}')
        self.root.resizable(True, True)

        self.board = []
        self.topRow = []

        for i in range(self.x_dimension):
            junk = []
            self.topRow.append(self.y_dimension-1)
            for j in range (self.y_dimension):
                junk.append(0)
            self.board.append(junk)

        print(self.board)

        self.currentPlayer = 1

        #Movement Buttons
        button0 = Button(self.root, text="Move Here", command = lambda: self.ButtonPress(0))
        button1 = Button(self.root, text="Move Here", command = lambda: self.ButtonPress(1))
        button2 = Button(self.root, text="Move Here", command = lambda: self.ButtonPress(2))
        button3 = Button(self.root, text="Move Here", command = lambda: self.ButtonPress(3))
        button4 = Button(self.root, text="Move Here", command = lambda: self.ButtonPress(4))
        button5 = Button(self.root, text="Move Here", command = lambda: self.ButtonPress(5))
        button6 = Button(self.root, text="Move Here", command = lambda: self.ButtonPress(6))
        
        # Movement Button Placement
        button0.grid(row = 0, column = 0)
        button1.grid(row = 0, column = 1)
        button2.grid(row = 0, column = 2)
        button3.grid(row = 0, column = 3)
        button4.grid(row = 0, column = 4)
        button5.grid(row = 0, column = 5)
        button6.grid(row = 0, column = 6)

        self.displayBoard()

        self.root.mainloop()

    def displayBoard(self):
        None

        canvas = Canvas(self.root, width=(95*self.x_dimension), height = (95*self.y_dimension))
        canvas.grid(row = 1, column = 0, columnspan = self.x_dimension, rowspan=self.y_dimension, sticky=NW)

        for columnNum, column in enumerate(self.board):

            for rowNum, entry in enumerate(column):

                if entry == 0:
                    canvas.create_rectangle(columnNum * 95, rowNum * 95, (columnNum+1)*95, (rowNum+1)*95, fill="white")
                elif entry == 1:
                    canvas.create_rectangle(columnNum * 95, rowNum * 95, (columnNum+1)*95, (rowNum+1)*95, fill="red")
                elif entry == 2:
                    canvas.create_rectangle(columnNum * 95, rowNum * 95, (columnNum+1)*95, (rowNum+1)*95, fill="blue")

        canvas.create_rectangle

    def ButtonPress(self, slot):
        
        self.board[slot][self.topRow[slot]] = self.currentPlayer

        self.topRow[slot] -= 1

        if (self.currentPlayer == 1):
            self.currentPlayer = 2
        else:
            self.currentPlayer = 1

        self.displayBoard()

        self.checkGameStatus(slot, self.topRow[slot]+1)

    def checkGameStatus(self, movex, movey):
        player = self.board[movex][movey]

        #Check Horizontal
        inRow = 1
        for num in range(1, self.connectNum):
            if (movex+num < self.x_dimension):
                if (self.board[movex+num][movey] == player):
                    inRow += 1
                else:
                    break

        for num in range(1, self.connectNum):
            if (movex-num >= 0):
                if (self.board[movex-num][movey] == player):
                    inRow += 1
                else:
                    break
        
        if (inRow >= self.connectNum):
            print(f"Player {player} Wins!")
            return 1 
            
        #Check Vertical
        inRow = 1
        for num in range(1, self.connectNum):
            if (movey+num < self.y_dimension):
                if(self.board[movex][movey+num] == player):
                    inRow += 1
                else:
                    break

        if (inRow >= self.connectNum):
            print(f"Player {player} Wins!")
            return 1 

        #Check Diagonal
    

if __name__ == "__main__":
    GUI()