from tkinter import *
import argparse
import numpy as np
import randomMove
import Minimax
import time

class Move:
    def __init__(self, player, column):
        self.player = player
        self.column = column

class GUI:
    def __init__(self):
        self.x_dimension = 7
        self. y_dimension = 6
        self.root=Tk()
        self.connectNum = 4

        self.gameMode = 1 # gameMode determines human v. human, human v. AI or AI v. AI

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

        self.gameStatusLabelText = StringVar()
        self.gameStatusLabelText.set("")
        gameStatusLabel = Label(self.root, textvariable=self.gameStatusLabelText, foreground="red")

        self.numGames = 0


        self.resetGame()

        self.displayMoveList()

        #Entry
        numGamesEntry = Entry(self.root, textvariable=self.numGames, font = ('calibre', 12, 'normal'), width = 10)

        #Movement Buttons
        button0 = Button(self.root, text="Move Here", command = lambda: self.MoveButtonPress(0))
        button1 = Button(self.root, text="Move Here", command = lambda: self.MoveButtonPress(1))
        button2 = Button(self.root, text="Move Here", command = lambda: self.MoveButtonPress(2))
        button3 = Button(self.root, text="Move Here", command = lambda: self.MoveButtonPress(3))
        button4 = Button(self.root, text="Move Here", command = lambda: self.MoveButtonPress(4))
        button5 = Button(self.root, text="Move Here", command = lambda: self.MoveButtonPress(5))
        button6 = Button(self.root, text="Move Here", command = lambda: self.MoveButtonPress(6))

        clearButton = Button(self.root, text="Clear Board", command = lambda: self.ClearButtonPress())
        AIMoveButton = Button(self.root, text="AI Move", command = lambda: self.getAIMove())
        runGameButton = Button(self.root, text="Run AI Game", command = lambda: self.runAIGame())
        runGameSetButton = Button(self.root, text="Run Game Set", command = lambda: self.runGameSet())
        
        # Movement Button Placement
        button0.grid(row = 1, column = 0)
        button1.grid(row = 1, column = 1)
        button2.grid(row = 1, column = 2)
        button3.grid(row = 1, column = 3)
        button4.grid(row = 1, column = 4)
        button5.grid(row = 1, column = 5)
        button6.grid(row = 1, column = 6)

        numGamesEntry.grid(row = 1, column = 10, sticky = W)

        gameStatusLabel.grid(row = 0, column = 0, columnspan = 8)

        clearButton.grid(row = 1, column = 7, columnspan = 1, sticky = NW)
        AIMoveButton.grid(row = 1, column = 8, columnspan=1, sticky = NW)
        runGameButton.grid(row = 1, column = 9, columnspan = 1, sticky = NW)
        runGameSetButton.grid(row = 1, column = 11, columnspan = 1, sticky = NW)

        self.displayBoard()

        self.root.mainloop()

    def displayMoveList(self):
        self.moveListText = Text(self.root, height=35, width = 30)
        for item in self.moveList:
            self.moveListText.insert(END, f"Player: {item.player} placed in slot: {item.column}\n")
        self.moveListText.grid(row = 2, column = 7, rowspan = 7, columnspan = 3, sticky = NW)

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
        
        self.numMoves += 1

        if (slot not in self.availableMoves):
            self.gameStatusLabelText.set("Non-Valid Move")
            print(f"Non Valid Move, Valid Moves: {self.availableMoves}")
            return
        
        self.board[slot][self.topRow[slot]] = self.currentPlayer
        self.topRow[slot] -= 1

        if self.topRow[slot] < 0:
            self.availableMoves.remove(slot)

        self.moveList.append(Move(self.currentPlayer, slot))

        if (self.currentPlayer == 1):
            self.currentPlayer = 2
        else:
            self.currentPlayer = 1

        self.displayBoard()

        result = self.checkGameStatus(slot, self.topRow[slot]+1)

        self.displayMoveList()

        if (self.gameMode == 1 and result == 0):

            self.getAIMove() 

    def getAIMove(self):

        self.numMoves += 1

        # Run AI Move Get, keep track of how much time AI took to process
        start_time = time.time()
        # slot = randomMove.randomMove(self.board, self.topRow, self.availableMoves, self.currentPlayer)
        slot = Minimax.minimax_move(self.board, self.topRow, self.availableMoves, self.currentPlayer, 6)
        print(f"AI Operation Took: {time.time() - start_time} seconds")
        self.timing[self.currentPlayer] += time.time() - start_time

        self.board[slot][self.topRow[slot]] = self.currentPlayer 

        self.topRow[slot] -= 1

        if self.topRow[slot] < 0:
            self.availableMoves.remove(slot)    

        self.moveList.append(Move(self.currentPlayer, slot))        

        if (self.currentPlayer == 1):
            self.currentPlayer = 2
        else:
            self.currentPlayer = 1

        self.displayBoard()

        result = self.checkGameStatus(slot, self.topRow[slot]+1)  

        self.displayMoveList() 

        return result               

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
            return player 
            
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
            return player 

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
            return player

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
            return player

        return 0                         

    def resetGame(self):
        self.board = []
        self.topRow = []
        self.availableMoves = []
        self.numMoves = 0
        self.timing = [0, 0, 0]
        self.moveList = []

        self.currentPlayer = 1

        self.gameStatusLabelText.set("")

        for i in range(self.x_dimension):
            junk = []
            self.availableMoves.append(i)
            self.topRow.append(self.y_dimension-1)
            for j in range (self.y_dimension):
                junk.append(0)
            self.board.append(junk) 

    def runAIGame(self):
        self.resetGame()
        while(True):
            result = self.getAIMove()
            self.root.update()
            if result != 0:
                self.gameFinished()
                return result
            
    def runGameSet(self):
        if self.numGames < 1:
            self.gameStatusLabelText.set(f"Error Number of Games Must be > 0")
            return
        
        
            

    def gameFinished(self):
        print(f"Game Took: {self.numMoves} Moves to Complete")
        print(f"Player 1 AI Took: {self.timing[1]} Seconds to Compute Moves")
        print(f"Player 2 AI Took: {self.timing[2]} Seconds to Compute Moves")

    def ClearButtonPress(self):
    
        print("clearing")

        self.gameFinished()

        self.resetGame()

        self.displayBoard()

        self.displayMoveList()

if __name__ == "__main__":
    GUI()
