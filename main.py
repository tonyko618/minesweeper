import numpy as np
import random as rn
import tkinter as tk
from solve import solve
from solve2 import solve2

class MainWindow:
    def __init__(self, master):
        self.master = master
        self.mainFrame = tk.Frame(master=master)
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
        MineGridArgs = [int(self.WidthEntry.get()), int(self.HeightEntry.get()), int(self.BombEntry.get())]
        GameWindow(self.mainFrame, self, MineGridArgs)
        self.master.withdraw()

class GameWindow:
    def __init__(self, master, parent, MineGridArgs):
        self.mainFrame = tk.Toplevel(master=master)
        self.parent = parent
        self.MineGridArgs = MineGridArgs
        self.mainFrame.protocol("WM_DELETE_WINDOW", self.Back)
        self.won = 0
        self.lost = 0

        self.InfoFrame = tk.Frame(master=self.mainFrame)
        self.InfoFrame.pack(fill=tk.X)
        self.BackButton = tk.Button(master=self.InfoFrame, text="Back", command=self.Back)
        self.BackButton.pack(side=tk.LEFT)
        self.RefreshButton = tk.Button(master=self.InfoFrame, text="Refresh", command=self.CreateMineGridFrame)
        self.RefreshButton.pack(side=tk.RIGHT)
        self.InfoLabel = tk.Label(master=self.InfoFrame, text=f"Bombs left: {MineGridArgs[2]}")
        self.InfoLabel.pack(side=tk.TOP)


        self.MineGridFrame = tk.Frame(master=self.mainFrame)
        self.MineGridSubFrame = tk.Frame(master=self.MineGridFrame)
        self.MineGridInstance = MineGrid(self.MineGridSubFrame, self, *self.MineGridArgs)
        self.MineGridFrame.pack()
        self.MineGridSubFrame.pack()

        self.HintButton = tk.Button(master=self.mainFrame, text="Hint", command=self.Hint)
        self.HintButton.pack()


    def CreateMineGridFrame(self):
        self.InfoLabel["text"] = f"Bombs left: {self.MineGridArgs[2]}"
        self.MineGridSubFrame.destroy()
        self.MineGridSubFrame = tk.Frame(master=self.MineGridFrame)
        self.MineGridInstance = MineGrid(self.MineGridSubFrame, self, *self.MineGridArgs)
        self.MineGridSubFrame.pack()
    
    def Back(self):
        self.parent.master.deiconify()
        self.mainFrame.destroy()

    def Hint(self):
        revealed = np.array([np.array([x.revealed for x in y]) for y in self.MineGridInstance.CellGrid])
        flagged = np.array([np.array([x.flagged for x in y]) for y in self.MineGridInstance.CellGrid])
        adj = np.array([np.array([x.adj for x in y]) for y in self.MineGridInstance.CellGrid])

        risk = solve(self.MineGridInstance.BombNum, self.MineGridInstance.BombNum-self.MineGridInstance.MarkedBombNum, revealed, flagged, adj)
        moved = False
        min = 255
        coord = (0,0)
        for x in range(self.MineGridArgs[0]):
            for y in range(self.MineGridArgs[1]):
                if not self.MineGridInstance.get(x,y).revealed and not self.MineGridInstance.get(x,y).flagged:
                    if risk[y,x] == 0:
                        self.MineGridInstance.get(x,y).LeftClick()
                        moved = True
                        continue
                    if risk[y,x] == 255:
                        self.MineGridInstance.get(x,y).RightClick()
                        moved = True
                        continue
                    hexadecimal = hex(255-risk[y,x])[2:]
                    hexadecimal = "#" + hexadecimal*3
                    self.MineGridInstance.get(x,y).button["bg"] = hexadecimal
                    if risk[y,x] <= min:
                        if (coord[0]-self.MineGridArgs[0]/2)**2 + (coord[1]-self.MineGridArgs[1]/2)**2 > (x-self.MineGridArgs[0]/2)**2 + (y-self.MineGridArgs[1]/2)**2:
                            min = risk[y,x]
                            coord = (x,y)

        if not moved:
            print("using alternative algorithm")
            risk = solve(self.MineGridInstance.BombNum, self.MineGridInstance.BombNum-self.MineGridInstance.MarkedBombNum, revealed, flagged, adj)
            for x in range(self.MineGridArgs[0]):
                for y in range(self.MineGridArgs[1]):
                    if not self.MineGridInstance.get(x,y).revealed and not self.MineGridInstance.get(x,y).flagged:
                        if risk[y,x] == 0:
                            self.MineGridInstance.get(x,y).LeftClick()
                            moved = True
                            continue
                        if risk[y,x] == 255:
                            self.MineGridInstance.get(x,y).RightClick()
                            moved = True
                            continue
                        

                
        """if not moved:
            self.MineGridInstance.get(*coord).LeftClick()
        if self.MineGridInstance.status == 0:
            self.parent.master.after(10, self.Hint)
        if self.MineGridInstance.status != 0:
            self.CreateMineGridFrame()
            self.parent.master.after(1000, self.Hint)"""


        


        


class MineGrid:
    def __init__(self, master, parent, width, height, BombNum):
        self.mainFrame = tk.Frame(master=master)
        self.mainFrame.pack()
        self.parent = parent
        self.width = width
        self.height = height
        self.BombNum = BombNum
        self.BombLeft = self.BombNum
        self.BombArray = [False]*(width*height)
        self.SafeLeft = width*height-BombNum
        self.MarkedBombNum = 0
        #0:ongoing game ,1:won, 2:lost
        self.status = 0
        

        for i in range(len(self.BombArray)):
            if self.BombLeft/(len(self.BombArray)-i) >= rn.random():
                self.BombArray[i] = True
                self.BombLeft -= 1

        self.SolutionGrid = np.array(self.BombArray).reshape(self.height, self.width)
        #print(self.SolutionGrid)

        self.CellGrid = []
        for i in range(self.height):
            self.CellArray = []
            self.frame = tk.Frame(master=self.mainFrame)
            self.frame.pack()
            for j in range(self.width):
                self.CellArray.append(Cell(master=self.frame, parent=self, x=j, y=i, bomb=self.SolutionGrid[i][j]))
            self.CellGrid.append(self.CellArray)
        


    def get(self, x, y):
        try:
            return self.CellGrid[y][x]
        except:
            class CellNotFound(Exception):
                pass
            raise CellNotFound(f"The coordinate {(x,y)} is not found, the size of the grid is {(self.width,self.height)}")

    def counter(self):
        self.SafeLeft -= 1
        if self.SafeLeft == 0:
            self.parent.InfoLabel["text"] = "You won!"
            self.status = 1
            self.parent.won += 1
            print(f"won: {self.parent.won}, lost: {self.parent.lost}")

class Cell:
    def __init__(self, master, parent, x, y, bomb):
        self.master = master
        self.parent = parent
        self.x = x
        self.y = y
        self.bomb = bomb
        self.flagged = False
        self.revealed = False
        self.adj = None

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
                    if x == self.x and y == self.y:
                        continue
                    output.append((x,y))
        return output

    
    def LeftClick(self, *event):
        if self.revealed or self.flagged:
            return
        else:
            self.revealed = True

        if self.bomb:
            self.button["bg"] = "red"
            self.parent.parent.InfoLabel["text"] = "You lost!"
            self.parent.status = 2
            self.parent.parent.lost += 1
            print(f"won: {self.parent.parent.won}, lost: {self.parent.parent.lost}")
            """for x in range(self.parent.width):
                for y in range(self.parent.height):
                    if self.parent.get(x,y).bomb:
                        self.parent.get(x,y).LeftClick()"""
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

    def RightClick(self, *event):
        if self.revealed:
            return
        if self.flagged:
            self.button["bg"] = "white"
            self.parent.MarkedBombNum -= 1
        else:
            self.button["bg"] = "blue"
            self.parent.MarkedBombNum += 1
        self.flagged = not self.flagged
        self.parent.parent.InfoLabel["text"] = f"Bombs left: {self.parent.BombNum - self.parent.MarkedBombNum}"
    




window = tk.Tk()
MainWindow(window)
window.mainloop()
