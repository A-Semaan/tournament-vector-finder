senders = []
receipients = []
givesTo = {}
receivesFrom = {}

#   functions

#   conversions
def binaryToDecimal(n):
    return int(n, 2)


def decimalToBinary(n):
    return bin(n).replace("0b", "")


def convertToTournament(matrix):
    size = len(matrix)
    toReturn = [0 for i in range(size)]
    for i in range(size-1):
        toReturn[i] = binaryToDecimal("".join(list(map(str, matrix[i]))))
    return toReturn


def convertToMatrix(tournament):
    size = len(tournament)
    toReturn = []
    tournamentBin = [0 for i in range(size)]
    for i in range(size):
        tournamentBin[i] = decimalToBinary(int(tournament[i]))
    for i in range(size-1):
        bins = [int(char) for char in str(tournamentBin[i])]
        if(len(bins) > (size-(i+1))) and i != size-1:
            return False
        else:
            while len(bins) < size:
                bins.insert(0, 0)
            toReturn.append(bins)
    toReturn.append([0 for i in range(size)])
    return toReturn


def invertMatrix(matrix):
    size = len(matrix)
    for i in range(size):
        for j in range(i, size):
            if(i == j):
                continue
            else:
                if matrix[i][j] == 0:
                    matrix[j][i] = 1
                elif matrix[i][j] == 1:
                    matrix[j][i] = 0
    return matrix


def showMatrixWithArcs(matrix):
    senders.clear()
    receipients.clear()
    givesTo.clear()
    receivesFrom.clear()

    size = len(matrix)
    for i in range(size):
        for j in range(size):
            if(i == j):
                continue
            else:
                if matrix[i][j] == 1:
                    incrementedI = i+1
                    incrementedJ = j+1
                    senders.append(incrementedI)
                    receipients.append(incrementedJ)
                    if(givesTo.get(incrementedI, -1) == -1):
                        givesTo[incrementedI] = [len(receipients)-1]
                    else:
                        givesTo[incrementedI].append(len(receipients)-1)
                    if(receivesFrom.get(incrementedJ, -1) == -1):
                        receivesFrom[incrementedJ] = [len(senders)-1]
                    else:
                        receivesFrom[incrementedJ].append(len(senders)-1)
        if(len(givesTo)!=i+1):
            givesTo[i+1]=[]
        if(len(receivesFrom)):
            receivesFrom[i+1]=[]
    tournament = getDirectedPathsAndMedianOrder(size)
    print("This tournament's directed paths are:\n")
    for string in tournament[0]:
        print("\t"+string)
    medianOrder=tournament[1]
    print("This tournament's median orders are having value of "+str(medianOrder["maxForwardArc"])+":\n")
    for string in medianOrder["medianOrder"]:
        print("\t"+string)


def getDirectedPathsAndMedianOrder(size):
    maxMedianOrder=0
    medianOrder=[]
    maxForwardArcs = 0
    directedPaths = []
    currentDirectedPaths = []
    for i in range(1, size+1):
        joinLists(currentDirectedPaths, getDirectedPathsStartingAt(
            "", currentDirectedPaths, i, size))
        for i in range(len(currentDirectedPaths)):
            currentArcCount = calculateMaxForwardArcs(currentDirectedPaths[i])
            if(currentArcCount > maxForwardArcs):
                directedPaths.clear()
                if(currentDirectedPaths[i] not in directedPaths):
                    directedPaths.append(currentDirectedPaths[i])
                maxForwardArcs = currentArcCount
            elif(currentArcCount == maxForwardArcs):
                if(currentDirectedPaths[i] not in directedPaths):
                    directedPaths.append(currentDirectedPaths[i])

            currentMedianOrder = calculateMedianOrder(currentDirectedPaths[i])
            if(currentMedianOrder>maxMedianOrder):
                medianOrder.clear()
                if(currentDirectedPaths[i] not in medianOrder):
                    medianOrder.append(currentDirectedPaths[i])
                maxMedianOrder = currentMedianOrder
            elif(currentMedianOrder==maxMedianOrder):
                if(currentDirectedPaths[i] not in medianOrder):
                    medianOrder.append(currentDirectedPaths[i])

    return [directedPaths,{
        "medianOrder":medianOrder,
        "maxForwardArc":maxMedianOrder
    }]


def joinLists(list1, list2):
    for string in list2:
        if string not in list1:
            list1.append(string)


def getDirectedPathsStartingAt(string, list, startAt, size):
    if string.count("v") == size-1:
        if(startAt > 0):
            string += " -> v"+str(abs(startAt))
        else:
            string += " <- v"+str(abs(startAt))
        return [string]
    else:
        if(string.count("v") == 0):
            string += "v"+str(abs(startAt))
        else:
            if(startAt > 0):
                string += " -> v"+str(abs(startAt))
            else:
                string += " <- v"+str(abs(startAt))
        possibleSteps = getNextPossibleSteps(abs(startAt))
        for i in possibleSteps:
            if str(abs(i)) not in string:
                joinLists(list, getDirectedPathsStartingAt(
                    string[:], list, i, size))
        return list


def getNextPossibleSteps(num):
    possibleSteps = []

    temp = givesTo[num]
    for i in temp:
        possibleSteps.append(receipients[i])
    temp = receivesFrom[num]
    for i in temp:
        possibleSteps.append(-senders[i])
    return possibleSteps


def getNextForwardPossibleStepsExcluding(num, exclude):
    possibleSteps = []

    temp = givesTo[num]
    for i in temp:
        if(receipients[i] != exclude):
            possibleSteps.append(receipients[i])
    return possibleSteps


def calculateMaxForwardArcs(median):
    return median.count("->")


def calculateMedianOrder(median):
    visibleForwardArcs = calculateMaxForwardArcs(median)
    remainingForwardArcs = calculateRemainingForwardArcs(median)
    return visibleForwardArcs+remainingForwardArcs


def calculateRemainingForwardArcs(median):
    temps = median.split("v")
    vertices = []
    for temp in temps:
        if(len(temp)>=1):
            vertices.append(int(temp[0]))
    counter=0;
    verticesClone = vertices.copy()
    for i in range(len(vertices)-1):
        forwardPossibleSteps = getNextForwardPossibleStepsExcluding(vertices[i],vertices[i+1])
        verticesClone.pop(0)
        for step in forwardPossibleSteps:
            if(verticesClone.count(step)>0):
                counter+=1

    return counter


def convertToArcedTournament(median):
    toReturn = ""
    for i in range(len(median)-1):
        if(i == 0):
            toReturn += "v"+str(median[i])
        toReturn += " <- v" + \
            str(median[i+1]) if median[i+1] < 0 else " -> v"+str(median[i+1])
    return toReturn


# main
if(__name__ == "__main__"):
    while True:
        operation = input(
            "\nPlease choose the operation:\nEnter 1 to search for representative Vector of T with respect to E=v1...vn\nEnter 2 to search for a Tournament relative to a vetor if it exists\n> ")
        if operation == "1" or operation == "2":
            break

    if operation == "1":
        # we enter the vector
        size = input("\nThe tournament is of order n\nPlease enter n:\n> ")
        size = int(size)
        vector = [[0 for col in range(size)] for row in range(size)]
        for i in range(1, size):
            vertices = input("\nPlease enter the indexes of the outneighbours of v" +
                             str(i)+" that are greater than "+str(i)+" separated by comma (example: 2,4,5):\n> ")
            if (isinstance(vertices,str) and vertices !="" and vertices !="0"):
                vertices = vertices.split(",")
                for vertexIndex in vertices:
                    vertexIndex = int(vertexIndex)
                    if(vertexIndex>size or vertexIndex<=i):
                        print("Invalid input")
                        exit()
                    vector[i-1][int(vertexIndex)-1] = 1

        tournament = convertToTournament(vector)
        matrix = invertMatrix(vector)
        print("Tournament:")
        for i in range(size):
            print("[", end="")
            print(tournament[i], end="")
            print("]")
        print("Matrix:")
        for i in range(size):
            print("[", end="")
            for j in range(size):
                print(matrix[i][j], end="")
            print("]")
        showMatrixWithArcs(matrix)
    else:
        # we enter the tournament
        size = input("\nThe vector is of order n\nPlease enter n:\n> ")
        size = int(size)
        tournament = [0 for row in range(size)]
        
        values = input(
            "\nPlease enter the decimal values of the tournament separated by comma (example: 6,1,1):\n> ")
        values = values.split(",")
        if len(values) > size:
            print("Invalid input")
            exit()
        elif len(values)==size:
            if values[size-1]!=0:
                print ("Input does not represent a valid tournament")
                exit()
        
        for i in range(size-1):
            tournament[i] = int(values[i])
            

        matrix = convertToMatrix(tournament)
        if(matrix == False):
            print("This is an invalid tournament")
            exit(0)
        else:
            vectorOutput = ""
            matrix = invertMatrix(matrix)
            for i in range(size):
                vertex = "(v"+str(i+1)+", "
                for j in range(size):
                    if(matrix[i][j] == 1):
                        if(vectorOutput==""):
                            vectorOutput+="E(T)= { "
                        else:
                            vectorOutput+=", "
                        vectorOutput += vertex+"v"+str(j+1)+")"
            vectorOutput+=" }"
            print("Matrix:")
            for i in range(size):
                print("[", end="")
                for j in range(size):
                    print(matrix[i][j], end="")
                print("]")
            print("Vector:")
            print(vectorOutput)
            showMatrixWithArcs(matrix)
