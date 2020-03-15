from queue import PriorityQueue
import math
import sys


class Pathfinding:

    # initializes all global variables that need to be attributes of the class
    def __init__(self, fileName, canDiagonal):

        # strips the filename so that the same function can read in both the text files a&b (diagonal/not)
        self.extension = ".txt"
        if fileName.endswith(self.extension):
            fileName = fileName[:-len(self.extension)]


        self.fileName = fileName  # holds the filename
        self.canDoDiagonal = canDiagonal # informs the function is diagonal movements are allowed

        self.grid = [] # an array that holds the grid from the text file
        self.startPosition = None # stores the value of the starting position marked as "S" on the grid
        self.goalPosition = None # stores the value of the goal position marked as "G" on the grid
        self.numRows = 0
        self.numColumns = 0

        self.path = [] # stores the recreated path travelled by the algorithms

        self.readFile() # initializes the read of the file and initializes the search algorithms

    # both reads the text file given and creates a new output file for all print statements to be sent to
    # initializes the search algorithms to begin with the information retrieved from the text files
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
                # The elements in the row separated into individual elements
                row = list(cleaned)

                # Determine column where the start position is, if available
                try:
                    indexOfS = row.index("S")
                except ValueError:
                    indexOfS = None

                # Determine column where the goal position is, if available
                try:
                    indexOfG = row.index("G")
                except ValueError:
                    indexOfG = None

                # Save the start and goal positions if available
                if indexOfS:
                    startPos = (indexOfS, n)
                if indexOfG:
                    goalPos = (indexOfG, n)

                # Determine number of columns in a row
                m = len(row)
                self.grid.append(list(cleaned))
                n += 1
            else:  # new grid
                self.runAlgorithms(m, n, startPos, goalPos)
                print()
                n = 0
                self.grid = []
                file.readline()

        # Last grid to run
        self.runAlgorithms(m, n, startPos, goalPos)

        sys.stdout = originalOutput

    def runAlgorithms(self, m, n, startPos, goalPos):
        self.numRows = n
        self.numColumns = m
        self.startPosition = startPos
        self.goalPosition = goalPos

        originalGrid = self.grid.copy()

        self.greedy()

        # Reset grid and path for new search (has no P for path found by A*)
        self.grid = originalGrid
        self.path = []

        self.AStar()

        # print()


    # returns the calculation performed by the heuristic calculation depending on whether on not
    # diagonal movement is allowed within the grid
    def heuristic(self, a, b):

        if self.canDoDiagonal:
            heuristic = self.euclidean(a, b)
        else:
            heuristic = self.manhattan(a, b)

        return heuristic

    # Euclidean heuristic used to calculate straight line distances (diagonals allowed)
    def euclidean(self, a, b):
        return math.sqrt(pow(a[0] - b[0], 2) + pow(a[1] - b[1], 2))

    # Manhattan heuristic used to calculate paths with no diagonal movements
    def manhattan(self, a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    # finds the neighbours of a given position and returns then as a list of tuples
    def getNeighbours(self, position):

        possibleMoves = []
                    # down,     up,     right,   left
        neighbours = [(0, 1), (0, -1), (1, 0), (-1, 0)]

        if self.canDoDiagonal:
                    #   down/right - down/left - up/right - up/left
            diagonals = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
            neighbours += diagonals

        for x, y in neighbours:

            # current position + possible new position (right or left or up or down...)
            newX = position[0] + x
            newY = position[1] + y

            # check that new position is within bounds
            if newX < 0 or newX >= self.numColumns:
                continue
            if newY < 0 or newY >= self.numRows:
                continue
            else:
                possibleMoves.append((newX, newY))

        return possibleMoves

    # performs the A* Algorithm using an accumulating cost and a priority queue
    def AStar(self):

        # built in priority queue class that stores the values based on increasing priority (minimum at front)
        frontier = PriorityQueue()
        frontier.put(self.startPosition, 0)
        # tracks where the current node came from
        cameFrom = {self.startPosition: None}
        # tracks the accumulated cost of the current position
        costSoFar = {self.startPosition: 0}

        # For as long as there are positions in the list
        while not frontier.empty():
            # Get the first (top priority) position
            current = frontier.get()

            # Break if the current position is the goal position
            if current == self.goalPosition:
                break

            # Check all available positions neighbouring current most ideal position
            for nextNeighbour in self.getNeighbours(current):
                row = nextNeighbour[1]
                col = nextNeighbour[0]

                neighbourValue = ''
                try:
                    neighbourValue = self.grid[row][col]
                except IndexError:
                    print(row, col)

                # Determine the cost of taking the neighbour position
                newCost = costSoFar[current] + self.getCost(neighbourValue)

                # Add to queue if it hasn't already been included or the new cost is better than the old cost
                if neighbourValue is not 'X':
                    if nextNeighbour not in costSoFar or newCost < costSoFar[nextNeighbour]:
                        # Update cost
                        costSoFar[nextNeighbour] = newCost
                        # Determine priority based on heuristic
                        priority = newCost + self.heuristic(self.goalPosition, nextNeighbour)
                        # Add the neighbour and its priority to the queue
                        frontier.put(nextNeighbour, priority)
                        # Update the path from the neighbour position
                        cameFrom[nextNeighbour] = current

        # rebuilds the path that we took to get from the goal to the start and reverses it so it can be printed in order
        current = self.goalPosition
        self.path = [current]

        # Continue following the path backwards until the current position is the goal position
        while current != self.startPosition:
            current = cameFrom[current]
            self.path.append(current)
        # self.path.append(self.startPosition)
        self.path.reverse()

        self.printGrid("A*")

    def greedy(self):
        # built in priority queue class that stores the values based on increasing priority (minimum at front)
        frontier = PriorityQueue()
        frontier.put(self.startPosition, 0)
        # tracks where the current node came from
        cameFrom = {self.startPosition: None}

        # For as long as there are positions in the list
        while not frontier.empty():
            # Get the first (top priority) position
            current = frontier.get()

            # Break if the current position is the goal position
            if current == self.goalPosition:
                break

            # Check all available positions neighbouring current most ideal position
            for nextNeighbour in self.getNeighbours(current):
                row = nextNeighbour[1]
                col = nextNeighbour[0]

                neighbourValue = ''
                try:
                    neighbourValue = self.grid[row][col]
                except IndexError:
                    print(row, col)

                # Add to the queue if the neighbour isn't a boundary and isn't already a visited value
                if neighbourValue is not 'X' and nextNeighbour not in cameFrom:
                    # Determine the priority based on the heuristic
                    priority = self.heuristic(self.goalPosition, nextNeighbour)
                    # Add the neighbour and its priority to the queue
                    frontier.put(nextNeighbour, priority)
                    # Update the path from the neighbour position
                    cameFrom[nextNeighbour] = current

        # rebuilds the path that we took to get from the goal to the start and reverses it so it can be printed in order
        current = self.goalPosition
        self.path = [current]

        # Continue following the path backwards until the current position is the goal position
        while current != self.startPosition:
            current = cameFrom[current]
            self.path.append(current)
        # self.path.append(self.startPosition)
        self.path.reverse()

        self.printGrid("Greedy")

    # a cost function that takes a neighbourValue which is either "X" or "_" meaning it is viable or it is a boundary
    def getCost(self, neighbourValue):

        # if it is a boundary create a high cost so that it will never be chosen as A* chooses minimum
        if neighbourValue is 'X':
            return 100

        # else if it is a viable movement make the cost one as any right, left, up, down is one movement
        else:
            return 1

    # Prints the grid to the output file with the name of the algorithm that solved the path
    def printGrid(self, algorithm):
        print(algorithm)

        for row in range(self.numRows):
            for col in range(self.numColumns):
                # Determine the value
                value = self.grid[row][col]

                # If the position is in the path
                if (col, row) in self.path:
                    # Change the value to 'P' for Path if not already start or goal
                    if value is not 'S' and value is not 'G':
                        value = 'P'

                print(value, end="")
            print()


if __name__ == '__main__':
    pathfindingA = Pathfinding("pathfinding_a.txt", False)
    pathfindingB = Pathfinding("pathfinding_b.txt", True)
