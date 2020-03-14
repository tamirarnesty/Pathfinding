import sys
import math


class AlphaBeta:

    # initializes all of the lists and variables necessary to store function information
    def __init__(self, fileName):

        self.fileName = fileName
        self.count = 0
        self.MAX = [] # stores all nodes that are the labelled as maximum comparison
        self.MIN = [] # stores all nodes that are the labelled as minimum comparison
        self.result = [] # temporarily stores the cleaned data from the text file
        self.leafNodes = [] # stores a list of all leaf node integers
        self.allNodes = [] # stores a list of all the nodes
        self.readFile() # initializes the reading of the file which prompts the algorithm

    # cleans the data file by creating a list of tuples where each element is a coordinate pair
    def cleanString(self, string):
        return [tuple(str(i) for i in element.strip('()').split(',')) for element in string.split('),(')]

    # creates the list of max and min node comparisons
    def findMaxMin(self):

        for item in self.result:
            if item[1] == "MAX":
                self.MAX.append(item[0])
            elif item[1] == "MIN":
                self.MIN.append(item[0])
            else:
                break

    # creates the list of all leaf nodes and type casts it from strings to integers
    def findLeafNodes(self):

        for element in self.result:

            if element[0] not in self.allNodes:
                self.allNodes.append(element[0])

            # accounts for negative numbers and positive
            if element[1].lstrip("-").isdigit():
                self.leafNodes.append(int(element[1]))


    # takes a specified node (the current node) and returns its children
    def children(self, node):

        children = []
        for element in self.result:
            if element[0] == node:
                # checks if the node is a digit and type casts it to integer if it is
                if element[1].lstrip("-").isdigit():
                    children.append(int(element[1]))
                # otherwise simply appends value as a string
                else:
                    children.append(element[1])

        return children


    # this function is responsible for invoking the algorithm by first reading in the text file and then outputting it
    # to the new output file "alphabeta_out.txt"
    def readFile(self):

        # open the file and read it line by line, as well as initialize the file to write the output to
        file = open(self.fileName, 'r')
        cleanFile = file.readlines()
        sys.stdout = open("alphabeta_out.txt", "w")

        # this number tracks which graph from the text file we are currently analyzing
        num = 1


        for i in cleanFile:
            # for every line strip the white space character and split the sets by space characters
            x = i.strip()
            stripped = x.split(" ")

            # for each set split by the space character, strip the set brackets
            # and clean the string to return list of tuples
            for row in stripped:
                string = row.strip("{}")
                self.result = self.cleanString(string)
                # print(self.result)
                self.findMaxMin()
                self.findLeafNodes()

            # prints the output in the required format
            print("Graph: ", num, "Score: ", self.alphaBeta(self.allNodes[0], -math.inf, math.inf)
                  , "Leaf Nodes Examined: ", self.count)


            # reinitialize variables for new graph analysis
            self.count = 0
            self.allNodes = []
            self.leafNodes = []
            self.MAX = []
            self.MIN = []
            num += 1

        sys.stdout.close()
        file.close()


    # this function takes the node we are currently analyzing as well as the alpha and beta values
    # and returns the score that is achieved by running the algorithm on the given tree
    def alphaBeta(self, currentNode, alpha, beta):

        # finds all the children of the given node
        children = self.children(currentNode)


        # if the node is a leaf node, increase the number of leaf nodes examined
        if currentNode in self.leafNodes:
            self.count += 1
            return currentNode

        # if it belongs to maximum list, perform a maximum comparison
        # where at the beginning the best possible value is -infinity
        if currentNode in self.MAX:
            bestValue = -math.inf

            # for each child iterate down the branches and determine if a better value can be found
            for child in children:
                value = self.alphaBeta(child, alpha, beta)
                bestValue = max(bestValue, value)
                alpha = max(alpha, bestValue)
                # if the alpha value is better than beta cut off the search at the given node
                if alpha >= beta:
                    break

            #return the best score so far
            return bestValue

        else:
            #if currentNode in self.MIN:   perform the minimum comparison where the best value is infinity to begin
            bestValue = math.inf

            # for each child iterate down the branches and determine if a better value can be found
            for child in children:
                value = self.alphaBeta(child, alpha, beta)
                bestValue = min(bestValue, value)
                beta = min(beta, bestValue)
                # if the alpha value is better than beta cut off the search at the given node
                if beta <= alpha:
                    break

            # return the best score so far
            return bestValue

if __name__ == '__main__':
    pruning = AlphaBeta("alphabeta.txt")
