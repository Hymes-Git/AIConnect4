from tkinter import *
import argparse
import numpy as np
import randomMove

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

        self.gameStatusLabelText = StringVar()
        self.gameStatusLabelText.set("")
        gameStatusLabel = Label(self.root, textvariable=self.gameStatusLabelText, foreground="red")


        #Movement Buttons
        button0 = Button(self.root, text="Move Here", command = lambda: self.MoveButtonPress(0))
        button1 = Button(self.root, text="Move Here", command = lambda: self.MoveButtonPress(1))
        button2 = Button(self.root, text="Move Here", command = lambda: self.MoveButtonPress(2))
        button3 = Button(self.root, text="Move Here", command = lambda: self.MoveButtonPress(3))
        button4 = Button(self.root, text="Move Here", command = lambda: self.MoveButtonPress(4))
        button5 = Button(self.root, text="Move Here", command = lambda: self.MoveButtonPress(5))
        button6 = Button(self.root, text="Move Here", command = lambda: self.MoveButtonPress(6))

        clearButton = Button(self.root, text="Clear Board", command = lambda: self.ClearButtonPress())
        
        # Movement Button Placement
        button0.grid(row = 1, column = 0)
        button1.grid(row = 1, column = 1)
        button2.grid(row = 1, column = 2)
        button3.grid(row = 1, column = 3)
        button4.grid(row = 1, column = 4)
        button5.grid(row = 1, column = 5)
        button6.grid(row = 1, column = 6)

        gameStatusLabel.grid(row = 0, column = 0, columnspan = 8)

        clearButton.grid(row = 1, column = 7)

        self.displayBoard()

        self.root.mainloop()

    def displayBoard(self):
        None

        canvas = Canvas(self.root, width=(100*self.x_dimension), height = (100*self.y_dimension))
        canvas.grid(row = 2, column = 0, columnspan = self.x_dimension, rowspan=self.y_dimension, sticky=NW)

        for columnNum, column in enumerate(self.board):

            for rowNum, entry in enumerate(column):

                if entry == 0:
                    canvas.create_rectangle(columnNum * 100, rowNum * 100, (columnNum+1)*100, (rowNum+1)*100, fill="white")
                elif entry == 1:
                    canvas.create_rectangle(columnNum * 100, rowNum * 100, (columnNum+1)*100, (rowNum+1)*100, fill="red")
                elif entry == 2:
                    canvas.create_rectangle(columnNum * 100, rowNum * 100, (columnNum+1)*100, (rowNum+1)*100, fill="blue")

        canvas.create_rectangle

    def MoveButtonPress(self, slot):

        if (self.topRow[slot] < 0):
            self.gameStatusLabelText.set("Non-Valid Move")
            print("Non Valid Move")
            return
        
        self.board[slot][self.topRow[slot]] = self.currentPlayer

        self.topRow[slot] -= 1

        if (self.currentPlayer == 1):
            self.currentPlayer = 2
        else:
            self.currentPlayer = 1

        self.displayBoard()

        self.checkGameStatus(slot, self.topRow[slot]+1)

        slot = randomMove.randomMove(self.board, self.topRow)

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
            self.gameStatusLabelText.set(f"Player {player} Wins!")
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
            self.gameStatusLabelText.set(f"Player {player} Wins!")
            print(f"Player {player} Wins!")
            return 1 

        #Check Diagonal Left Up Right Down
        inRow = 1
        for num in range(1, self.connectNum): # Left Up
            if (movex - num >= 0 and movey - num >= 0):
                if (self.board[movex-num][movey-num] == player):
                    inRow += 1
                else:
                    break

        for num in range(1, self.connectNum): # Right Down
            if (movex + num < self.x_dimension and movey + num < self.y_dimension):
                if (self.board[movex+num][movey+num] == player):
                    inRow += 1
                else:
                    break

        if (inRow >= self.connectNum):
            self.gameStatusLabelText.set(f"Player {player} Wins!")
            print(f"Player {player} Wins!")
            return 1

        #Check Diagonal Right Up Left Down
        inRow = 1
        for num in range(1, self.connectNum): # Right Up
            if (movex + num < self.x_dimension and movey - num >= 0):
                if (self.board[movex+num][movey-num] == player):
                    inRow += 1
                else:
                    break

        for num in range(1, self.connectNum): # Left Down
            if (movex - num >= 0 and movey + num < self.y_dimension):
                if (self.board[movex-num][movey+num] == player):
                    inRow += 1
                else:
                    break

        if (inRow >= self.connectNum):
            self.gameStatusLabelText.set(f"Player {player} Wins!")
            print(f"Player {player} Wins!")
            return 1                         
        

    def ClearButtonPress(self):
    
        print("clearing")

        self.board = []
        self.topRow = []

        self.currentPlayer = 1

        for i in range(self.x_dimension):
            junk = []
            self.topRow.append(self.y_dimension-1)
            for j in range (self.y_dimension):
                junk.append(0)
            self.board.append(junk)

        self.displayBoard()

if __name__ == "__main__":
    GUI()