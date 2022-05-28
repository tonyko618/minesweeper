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


def solve2(TotalBomb, BombLeft, revealed, flagged, adj):
    if False:
        print("-------------------------------------------")
        print("revealed:\n", revealed)
        print("flagged:\n", flagged)
        print("adj:\n", adj)
        print("BombLeft: ", BombLeft)
        print("TotalBomb: ", TotalBomb)

    width = len(revealed[0])
    height = len(revealed)
    output = np.zeros(shape=(height, width), dtype=np.int32)
    output.fill(int(TotalBomb/width/height*255))
  

    #print(output)
    return output

