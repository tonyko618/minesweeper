from logging import exception
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
        print(self)
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

        self.__TFGrid = np.array(self.__BombArray).reshape(self.height, self.width)
        print(self.__TFGrid)

        self.__CellGrid = []
        for i in range(self.height):
            self.CellArray = []
            self.frame = tk.Frame(master=self.mainFrame)
            self.frame.pack()
            for j in range(self.width):
                self.CellArray.append(Cell(master=self.frame, grid=self.get, x=j, y=i, width=self.width, height=self.height))
            self.__CellGrid.append(self.CellArray)
        


    def get(self, x, y):
        try:
            return self.__CellGrid[y][x]
        except:
            class CellNotFound(exception):
                pass
            raise CellNotFound(f"The coordinate {(x,y)} is not found, the size of the grid is {(self.width+1,self.height+1)}")



class Cell:
    def __init__(self, master, grid, x, y, width, height):
        self.master = master
        self.grid = grid
        self.x = x
        self.y = y
        self.GridWidth = width
        self.GridHeight = height
        self.flagged = False
        self.revealed = False

        self.frame = tk.Frame(master=self.master, width=30, height=30)
        self.frame.pack(side=tk.LEFT)
        self.button = tk.Button(master=self.frame, text="")
        self.button.bind("<Button-1>", self.LeftClick)
        self.button.bind("<Button-3>", self.RightClick)
        self.button.place(x=0, y=0, width=30, height=30)


    
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
                    if x<0 or y<0 or y>=self.GridHeight or x>=self.GridWidth:
                        continue
                    if self.grid(y,x):
                        self.adj += 1
  
            self.button["text"] = str(self.adj)
            if self.adj == 0:
                for x in range(self.x-1, self.x+2):
                    for y in range(self.y-1, self.y+2):
                        if x<0 or y<0 or y>=len(self.grid) or x>=len(self.grid[0]):
                            continue
                        self.cells[y][x].LeftClick()   

    def RightClick(self, event):
        if self.revealed:
            return
        self.button["bg"] = "blue"
    




window = tk.Tk()
MainWindow(window)
def Click(event):
    print(event)
window.bind("<KeyRelease>",Click)
window.mainloop()
