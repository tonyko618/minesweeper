import numpy as np
import random as rn
from solve import solve

width = input("enter the width of the grid")
height = input("enter the height of the grid")
BombNum = input("enter the total number of bombs")

BombArray = np.zeros((width*height), dtype=bool)
length = width*height
BombLeft = BombNum
for i in range(length):
    if BombLeft/(length-i) >= rn.random():
        BombArray[i] = True
        BombLeft -= 1
solution = BombArray.reshape(height, width)

