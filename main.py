import numpy as np
import random as rn
import tkinter as tk

class MainWindow:
    def __init__(self, master):
        self.master=master
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

        self.StartButton = tk.Button(master=self.mainFrame, text="Start", command=self.__ButtonClick)
        self.StartButton.pack()
    
    def __ButtonClick(self):
        GameFrame(self.master, int(self.WidthEntry.get()), int(self.HeightEntry.get()), int(self.BombEntry.get()))
        #GameFrame(self.master,10,10,10)
        window.withdraw()

class GameFrame:
    def __init__(self, master, width, height, BombNum):
        self.mainFrame = tk.Toplevel(master=master)
        self.width = width
        self.height = height
        self.BombNum = BombNum
        self.__BombLeft = self.BombNum
        self.__BombArray = [False]*(width*height)
        

        for i in range(len(self.__BombArray)):
            if self.__BombLeft/(len(self.__BombArray)-i) >= rn.random():
                self.__BombArray[i] = True
                self.__BombLeft -= 1

        self.__BombGrid = np.array(self.__BombArray).reshape(self.height, self.width)
        print(self.__BombGrid)

        self.__CellGrid = []
        for i in range(self.height):
            self.__CellGrid.append(Row(master=self.mainFrame, BombArray=self.__BombArray[self.width*i:self.width*(i+1)], grid=self.__BombGrid, y=i))
        
        for row in self.__CellGrid:
            row.CellReference(self.__CellGrid)




class Row:
    def __init__(self, master, BombArray, grid, y):
        self.master = master
        self.BombArray = BombArray
        self.grid = grid
        self.y = y
        self.length = len(self.BombArray)
        self.frame = tk.Frame(master=self.master)
        self.frame.pack()

        self.CellArray = []
        for i in range(self.length):
            self.CellArray.append(Cell(master=self.frame, bomb=self.BombArray[i], grid=self.grid, x=i, y=self.y))
    def __getitem__(self, num):
        return self.CellArray[num]

    def CellReference(self, cells):
        self.cells = cells
        for cell in self.CellArray:
            cell.CellRef(self.cells)

class Cell:
    def __init__(self, master, bomb, grid, x, y):
        self.master = master
        self.bomb = bomb
        self.grid = grid
        self.x = x
        self.y = y
        self.flagged = False
        self.revealed = False

        self.frame = tk.Frame(master=self.master, width=30, height=30)
        self.frame.pack(side=tk.LEFT)
        self.button = tk.Button(master=self.frame, text="")
        self.button.bind("<Button-1>", self.LeftClick)
        self.button.bind("<Button-3>", self.RightClick)
        self.button.place(x=0, y=0, width=30, height=30)

    def CellRef(self, cells):
        self.cells = cells
    
    def LeftClick(self, event=0):
        if self.revealed:
            return
        else:
            self.revealed = True

        if self.bomb:
            self.button["bg"] = "red"
        else:
            self.button["bg"] = "green"
            self.adj = 0
            for x in range(self.x-1, self.x+2):
                for y in range(self.y-1, self.y+2):
                    if x<0 or y<0 or y>=len(self.grid) or x>=len(self.grid[0]):
                        continue
                    if self.grid[y,x]:
                        self.adj += 1
  
            self.button["text"] = str(self.adj)
            if self.adj == 0:
                for x in range(self.x-1, self.x+2):
                    for y in range(self.y-1, self.y+2):
                        if x<0 or y<0 or y>=len(self.grid) or x>=len(self.grid[0]):
                            continue
                        self.cells[y][x].LeftClick()   

    def RightClick(self, event):
        self.button["bg"] = "blue"



window = tk.Tk()
MainWindow(window)
window.mainloop()
