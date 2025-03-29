from tkinter import *
import argparse

def main():

    # Create GUI and Title 
    root = Tk()
    root.title("Connect 4")

    # adjust the height and width of the window
    windowWidth = 1280
    windowHeight = 720
    screenWidth = root.winfo_screenwidth()
    screenHeight = root.winfo_screenheight()
    centerX = int(screenWidth/2 - windowWidth / 2)
    centerY = int(screenHeight/2 - windowHeight / 2)
    root.minsize(int(screenWidth / 4), int(screenHeight / 4))  # width, height
    root.maxsize(screenWidth,screenHeight)
    root.geometry(f'{windowWidth}x{windowHeight}')
    root.resizable(True, True)





    #Movement Buttons
    button0 = Button(root, text="Move Here", command = lambda: ButtonPress(0))
    button1 = Button(root, text="Move Here", command = lambda: ButtonPress(1))
    button2 = Button(root, text="Move Here", command = lambda: ButtonPress(2))
    button3 = Button(root, text="Move Here", command = lambda: ButtonPress(3))
    button4 = Button(root, text="Move Here", command = lambda: ButtonPress(4))
    button5 = Button(root, text="Move Here", command = lambda: ButtonPress(5))
    button6 = Button(root, text="Move Here", command = lambda: ButtonPress(6))
    
    # Movement Button Placement
    button0.grid(row = 0, column = 0)
    button1.grid(row = 0, column = 1)
    button2.grid(row = 0, column = 2)
    button3.grid(row = 0, column = 3)
    button4.grid(row = 0, column = 4)
    button5.grid(row = 0, column = 5)
    button6.grid(row = 0, column = 6)

    root.mainloop()

def ButtonPress(Slot):
    None


if __name__ == "__main__":
    main()