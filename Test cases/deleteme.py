# test.py
import sys
from random import randint


def createGrid(row, col):
    start = (randint(1, row-3), randint(1, col-3))
    goal = (randint(1, row-3), randint(1, col-3))
    while (goal == start):
        goal = (randint(1, row-3), randint(1, col-3))
    for i in range(col):
        print("X", end="")
    for j in range(row-2):
        print()
        print("X", end="")
        for k in range(col-2):
            chanceOfX = randint(1, 9)
            if start == (j, k):
                print("S", end = "")
            elif goal == (j, k):
                print("G", end = "")
            elif chanceOfX == 3:
                print("X", end="")
            else:
                print("_", end="")
        print("X", end="")
    print()
    for x in range(col):
        print("X", end="")
    print('\n')

if __name__ == "__main__":
    sys.stdout = open("insane.txt", 'w')
    for i in range(10):
        createGrid(1024, 1024)
