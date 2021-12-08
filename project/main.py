senders = []
receipients = []
givesTo = {}
receivesFrom={}

# functions
def binaryToDecimal(n):
    return int(n, 2)


def decimalToBinary(n):
    return bin(n).replace("0b", "")


def convertToTournament(vector):
    size = len(vector)
    toReturn = [0 for i in range(size)]
    for i in range(size-1):
        toReturn[i] = binaryToDecimal("".join(list(map(str, vector[i]))))
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
        for j in range(i,size):
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
                    if(givesTo.get(incrementedI,-1)==-1):
                        givesTo[incrementedI]=[len(senders)-1]
                    else:
                        givesTo[incrementedI].append(len(senders)-1)
                    if(receivesFrom.get(incrementedJ,-1)==-1):
                        receivesFrom[incrementedJ]=[len(receipients)-1]
                    else:
                        receivesFrom[incrementedJ].append(len(receipients)-1)
    tournament = getBestMedian(size)
    print(tournament) 

def getBestMedian(size):
    maxForwardArcs = 0
    bestMedian=""
    for i in range(size):
        median = getMedianStartingAt(i, size)
        calculatedMaxArcs = calculateMaxForwardArcs(median)
        if(calculatedMaxArcs>maxForwardArcs):
            maxForwardArcs=calculatedMaxArcs
            bestMedian=median
    return bestMedian

def getMedianStartingAt(startAt, size):
    maxForwardArcs=0
    
    actualStartAt = (startAt%size)+1
    nextVertex = actualStartAt
    bestMedian=""
    median=[]
    for i in range(size):
        median.append(nextVertex)
        nextVertex = getNextNodeFor(abs(nextVertex))
    median.append(nextVertex)

    strMedian = convertToArcedTournament(median)
    calculatedForwardArcs = calculateMaxForwardArcs(strMedian)
    if(calculatedForwardArcs>maxForwardArcs):
        maxForwardArcs=calculatedForwardArcs
        bestMedian = strMedian
        
    return bestMedian

def getNextNodeFor(i):
    if(givesTo.get(i,-1)!=-1):
        val = givesTo[i]
        givesTo.pop(i)
        receivesFrom.pop(i)
        return receipients[val[0]]
    elif(receivesFrom.get(i,-1)!=1):
        val = receivesFrom[i]
        givesTo.pop(i)
        receivesFrom.pop(i)
        return -senders[val[0]]
    return -1

def calculateMaxForwardArcs(median):
    return len(str(median).split("->"))-1

def convertToArcedTournament(median):
    toReturn=""
    for i in range(len(median)-1):
        if(i==0):
            toReturn+="v"+str(median[i])
        toReturn+= " <- v"+str(median[i+1]) if median[i+1]<0 else " -> v"+str(median[i+1])
    return toReturn
# main
if(__name__ == "__main__"):
    while True:
        operation = input(
            "\nPlease choose the operation:\nEnter 1 for Vector\nEnter 2 for Tournament\n> ")
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
            if vertices == "":
                vertices = "-1"
            vertices = vertices.split(",")
            for vertexIndex in vertices:
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

    else:
        # we enter the tournament
        size = input("\nThe vector is of order n\nPlease enter n:\n> ")
        size = int(size)
        tournament = [0 for row in range(size)]
        while True:
            values = input(
                "\nPlease enter the decimal values of the tournament separated by comma (example: 6,1,1):\n> ")
            values = values.split(",")
            if len(values) != size-1:
                print("Invalid input")
            else:
                for i in range(size-1):
                    tournament[i] = int(values[i])
                break

        matrix = convertToMatrix(tournament)
        if(matrix == False):
            print("This is an invalid tournament")
            exit(0)
        else:

            vectorOutput = ""
            matrix = invertMatrix(matrix)
            for i in range(size):
                vertexOutput = "v"+str(i+1)
                vertex = "\tv"+str(i+1)+" -> "
                for j in range(size):
                    if(matrix[i][j] == 1):
                        vertexOutput += vertex+"v"+str(j+1)+"\n"
                vectorOutput += vertexOutput
            print("Matrix:")
            for i in range(size):
                print("[", end="")
                for j in range(size):
                    print(matrix[i][j], end="")
                print("]")
            print("Vector:")
            print(vectorOutput)
            showMatrixWithArcs(matrix)
