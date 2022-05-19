#the function solve takes in 4 arguments
#the numbers of bombs left in unrevealed and unflagged cells (integer)
#revealed cells (array of boolean)
#cells that are marked to be bombs by the player (array of boolean)
#the number of bombs adjacent to a cell (array of integer) (the value would be None for cells that are not revealed yet)
#it should return an array of the same dimension, with integer values from 0 to 255
#0 indicates a cell have 0 probability to be a bomb
#255 indicates a cell is definitely a bomb

import numpy as np
import random as rn


def solve(BombLeft, revealed, flagged, adj):
    print("-------------------------------------------")
    print("revealed:\n", revealed)
    print("flagged:\n", flagged)
    print("adj:\n", adj)
    print("BombLeft: ", BombLeft)

    width = len(revealed[0])
    height = len(revealed)
    output = np.zeros(shape=(height, width), dtype=np.int32)
  

    def getNeighbour(x, y):
        output = []
        for x2 in range(x-1, x+2):
            for y2 in range(y-1, y+2):
                if x2>=0 and y2>=0 and y2<height and x2<width:
                    output.append((x2,y2))
        return output
    
    for x in range(width):
        for y in range(height):
            if revealed[y,x] and adj[y,x] and not flagged[y,x]:
                neighbour = getNeighbour(x,y)
                revealedNum = 0
                for x2, y2 in neighbour:
                    if revealed[y2,x2]:
                        revealedNum += 1
                if revealedNum == 8:
                    continue
                for x2, y2 in neighbour:
                    if not revealed[y2,x2]:
                        output[y2,x2] = max(output[y2,x2], adj[y,x]/(8-revealedNum)*255)





    print(output)
    return output

