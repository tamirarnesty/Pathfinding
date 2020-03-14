import sys
from math import sqrt
import heapq

class Pathfinding:

    def __init__(self, fileName, canDiagonal):
        self.extension = ".txt"
        if fileName.endswith(self.extension):
            fileName = fileName[:-len(self.extension)]
        self.fileName = fileName
        self.canDoDiagonal = canDiagonal
        self.grid = []
        self.start = None
        self.goal = None
        self.numRows = 0
        self.numColumns = 0
        self.readFile()

    def readFile(self):
        file = open(self.fileName + self.extension, 'r')
        originalOutput = sys.stdout
        outFileName = self.fileName + "_out" + self.extension
        sys.stdout = open(outFileName, 'w')
        m, n = 0, 0
        startPos = None
        goalPos = None
        lines = file.readlines()
        for i in range(len(lines)):
            cleaned = lines[i].strip()
            if cleaned != "":
                row = list(cleaned)
                try:
                    indexOfS = row.index("S")
                except ValueError:
                    indexOfS = None
                try:
                    indexOfG = row.index("G")
                except ValueError:
                    indexOfG = None
                if indexOfS:
                    startPos = (indexOfS, n) #(n, indexOfS)
                if indexOfG:
                    goalPos =  (indexOfG, n) #(n, indexOfG)
                m = len(row)
                self.grid.append(list(cleaned))
                n += 1
            else:  # new grid
                self.runAlgorithms(m, n, startPos, goalPos)
                n = 0
                self.grid = []
                file.readline()
        # Last grid to run
        self.runAlgorithms(m, n, startPos, goalPos)

        sys.stdout = originalOutput

    def runAlgorithms(self, m, n, startPos, goalPos):
        self.numRows = m
        self.numColumns = n
        self.startPosition = startPos
        self.goalPosition = goalPos
        self.AStar()
        self.greedy()
        print()

    def manhattenDistance(self, curPos):
        row, col = curPos
        rowDifference = abs(row - self.goal[0])
        colDifference = abs(col - self.goal[1])
        return rowDifference+colDifference

    def euclidenDistance(self, curPos):
        row, col = curPos
        rowDifference = abs(row - self.goal[0])
        colDifference = abs(col - self.goal[1])
        cSquared = rowDifference*rowDifference + colDifference*colDifference
        c = sqrt(cSquared)
        return c

    def AStar(self):
        self.printGrid("A*")
        frontier = [self.start]
        frontier = heapq.heapify(frontier)
        came_from = {} # use a dictionary to generate path by linkage
        came_from = {self.start}
        curPos = self.start
        while frontier != []:
            curPos = heapq.heappop(frontier)
            if curPos == self.goal:
                print("GOAL MOFOs")
                break
            r, c = curPos
            neighbors = [(r-1, c), (r+1, c), (r, c-1), (r, c+1)]
            for nextPos in neighbors:
                if nextPos not in came_from and self.grid[nextPos[0]][nextPos[1]] == "_":
                    if self.canDoDiagonal:
                        priority = self.euclidenDistance(curPos)
                    else:
                        priority = self.manhattenDistance(curPos)
                    heapq.heappush(frontier, (priority, nextPos))
                    came_from[nextPos[1]] = curPos

        # do the rest later --
    def greedy(self):
        self.printGrid("Greedy")
        pass

    def printGrid(self, algorithm):
        print(algorithm)
        for row in self.grid:
            for item in row:
                print(item, end="")
            print()


if __name__ == '__main__':
    pathfindingA = Pathfinding("pathfinding_a.txt", False)
    pathfindingB = Pathfinding("pathfinding_b.txt", True)
