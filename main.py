from logging import exception
import numpy as np
import random as rn
import tkinter as tk

class MainWindow:
    def __init__(self, master):
        self.master = master
        self.mainFrame = tk.Frame(master=self.master)
        self.mainFrame.pack()

        self.WidthFrame = tk.Frame(master=self.mainFrame)
        self.WidthLabel = tk.Label(master=self.WidthFrame, text="Width:")
        self.WidthEntry = tk.Entry(master=self.WidthFrame)
        self.WidthFrame.pack()
        self.WidthLabel.pack(side=tk.LEFT)
        self.WidthEntry.pack()

        self.HeightFrame = tk.Frame(master=self.mainFrame)
        self.HeightLabel = tk.Label(master=self.HeightFrame, text="Height:")
        self.HeightEntry = tk.Entry(master=self.HeightFrame)
        self.HeightFrame.pack()
        self.HeightLabel.pack(side=tk.LEFT)
        self.HeightEntry.pack()

        self.BombFrame = tk.Frame(master=self.mainFrame)
        self.BombLabel = tk.Label(master=self.BombFrame, text="Number of Bombs:")
        self.BombEntry = tk.Entry(master=self.BombFrame)
        self.BombFrame.pack()
        self.BombLabel.pack(side=tk.LEFT)
        self.BombEntry.pack()

        self.StartButton = tk.Button(master=self.mainFrame, text="Start", command=self.ButtonClick)
        self.StartButton.pack()
    
    def ButtonClick(self):
        GameFrame(self.master, int(self.WidthEntry.get()), int(self.HeightEntry.get()), int(self.BombEntry.get()))
        window.withdraw()

class GameFrame:
    def __init__(self, master, width, height, BombNum):
        print(self)
        self.mainFrame = tk.Toplevel(master=master)
        self.width = width
        self.height = height
        self.BombNum = BombNum
        self.BombLeft = self.BombNum
        self.BombArray = [False]*(width*height)
        self.SafeLeft = width*height-BombNum
        

        for i in range(len(self.BombArray)):
            if self.BombLeft/(len(self.BombArray)-i) >= rn.random():
                self.BombArray[i] = True
                self.BombLeft -= 1

        self.TFGrid = np.array(self.BombArray).reshape(self.height, self.width)
        print(self.TFGrid)

        self.CellGrid = []
        for i in range(self.height):
            self.CellArray = []
            self.frame = tk.Frame(master=self.mainFrame)
            self.frame.pack()
            for j in range(self.width):
                self.CellArray.append(Cell(master=self.frame, parent=self, x=j, y=i, bomb=self.TFGrid[i][j]))
            self.CellGrid.append(self.CellArray)
        


    def get(self, x, y):
        try:
            return self.CellGrid[y][x]
        except:
            class CellNotFound(exception):
                pass
            raise CellNotFound(f"The coordinate {(x,y)} is not found, the size of the grid is {(self.width+1,self.height+1)}")

    def counter(self):
        self.SafeLeft -= 1
        if self.SafeLeft == 0:
            print("you win")

class Cell:
    def __init__(self, master, parent, x, y, bomb):
        self.master = master
        self.parent = parent
        self.x = x
        self.y = y
        self.bomb = bomb
        self.flagged = False
        self.revealed = False

        self.frame = tk.Frame(master=self.master, width=30, height=30)
        self.frame.pack(side=tk.LEFT)
        self.button = tk.Button(master=self.frame, text="")
        self.button.bind("<Button-1>", self.LeftClick)
        self.button.bind("<Button-3>", self.RightClick)
        self.button.place(x=0, y=0, width=30, height=30)

    def neighbour(self):
        output = []
        for x in range(self.x-1, self.x+2):
            for y in range(self.y-1, self.y+2):
                if x>=0 and y>=0 and y<self.parent.height and x<self.parent.width:
                    output.append((x,y))
        return output

    
    def LeftClick(self, *event):
        if self.revealed or self.flagged:
            return
        else:
            self.revealed = True

        if self.bomb:
            self.button["bg"] = "red"
            print("you lost")
        else:
            self.parent.counter()
            self.button["bg"] = "green"
            self.adj = 0
            for (x, y) in self.neighbour():
                if self.parent.get(x,y).bomb:
                    self.adj += 1
  
            self.button["text"] = str(self.adj)
            if self.adj == 0:
                for (x, y) in self.neighbour():
                    self.parent.get(x,y).LeftClick()  

    def RightClick(self, event):
        if self.revealed:
            return
        
        if self.flagged:
            self.button["bg"] = "white"
        else:
            self.button["bg"] = "blue"
        self.flagged = not self.flagged
    




window = tk.Tk()
MainWindow(window)
window.mainloop()
