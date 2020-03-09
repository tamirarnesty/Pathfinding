import sys


class Pathfinding:

    def __init__(self, fileName, canDiagonal):
        self.extension = ".txt"
        if fileName.endswith(self.extension):
            fileName = fileName[:-len(self.extension)]

        self.fileName = fileName
        self.canDoDiagonal = canDiagonal

        self.grid = []
        self.startPosition = None
        self.goalPosition = None
        self.numRows = 0
        self.numColumns = 0

        self.readFile()

    def readFile(self):
        file = open(self.fileName + self.extension, 'r')

        originalOutput = sys.stdout
        outFileName = self.fileName + "_out" + self.extension
        sys.stdout = open(outFileName, 'w')

        m = 0
        n = 0

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
                    startPos = (n, indexOfS)
                if indexOfG:
                    goalPos = (n, indexOfG)

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

    def AStar(self):
        self.printGrid("A*")
        pass

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
