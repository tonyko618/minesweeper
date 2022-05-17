#the function solve takes in 4 arguments
#the total number of bombs in the grid (integer)
#revealed cells (array of boolean)
#cells that are marked to be bombs by the player (array of boolean)
#the number of bombs adjacent to a cell (array of integer) (the value would be None for cells that are not revealed yet)
#it should return an array of the same dimension, with integer values from 0 to 255
#0 indicates a cell have 0 probability to be a bomb
#255 indicates a cell is definitely a bomb

import numpy as np
def solve(TotalBombBUm, revealed, flagged, adj):
    print("-------------------------------------------")
    print("revealed:\n", revealed)
    print("flagged:\n", flagged)
    print("adj:\n", adj)
    print("TotalBombBUm: ", TotalBombBUm)

    width = len(revealed[0])
    height = len(revealed)
    output = np.zeros(shape=(height, width), dtype=np.int32)









    print(output)
    return output
