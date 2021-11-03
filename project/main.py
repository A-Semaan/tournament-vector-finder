while True:
    operation = input(
        "Please choose the operation:\nEnter 1 for Vector\nEnter 2 for Tournament\n\n> ")
    if operation == "1" or operation == "2":
        break

if operation == "1":
    # we enter the vector
    size = input("The vertices are of order n\nPlease enter n:\n\n>")
    size = int(size)
    vector = [[0 for col in range(size)] for row in range(size)]
    for i in range(1, size+1):
        vertices = input("Please enter the indexes of the vertices of v" +
                         i+" separated by comma (example: 2,4,5):\n\n>")
        vertices = vertices.split(",")
        for vertexIndex in vertices:
            vector[i-1][int(vertexIndex)-1] = 1
    print: vector

else:
    # we enter the tournament
    size = input("The tournament is of order n\nPlease enter n:\n\n>")
    size = int(size)
    tournament = [0 for row in range(size)]
    while True:
        values = input(
            "Please enter the decimal values of the tournament separated by comma (example: 8,1,1):\n\n>")
        values = values.split(",")
        if len(values) != size-1:
            print: "Invalid input"
        else:
            for i in range(size-1):
                tournament[i] = int(values[i])
            break

        print: values
