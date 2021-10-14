# This is a simple jigsaw puzzle solver.

import random
import sys, numpy, copy


def print_hi(name):
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


def create_array(filename):
    # Getting number of lines in order to create an array of every single line
    num_lines = len(open(filename).read().splitlines())
    print("Number of lines: " + str(num_lines))

    filelines = open(filename).read().splitlines()

    height = filelines[0].split(" ")[0]
    width = filelines[0].split(" ")[1]

    # Eliminate Height and Width from the pieces array
    filelines.pop(0)

    array = []
    for line in filelines:
        splitedline = line.split(" ")
        piece = []
        piece.append(splitedline)
        # You can rotate the pieces, so, let's add all possibilities here:
        for x in range(1,4):
            rotation = splitedline[x:]+splitedline[:x]
            piece.append(rotation)

        # Doing it this way, will create a 3D array.
        # This way, we have sides inside each piece rotation,
        # rotations inside pieces and pieces inside the puzzle
        # (sides->rotations->pieces)
        array.append(piece)

    # height = array[0][0]
    # width = array[0][1]

    return height, width, array


def solve(height, width, pieces):
    print("Height: " + height)
    print("Width: " + width)

    # print("Possible pieces: \n", array)


    # I will try a code using the backtracing method
    # Each piece can be united to another which has
    # a side in common in the correct position

    # I will try searching every possible combination

    # We will start by getting a random piece:
    # The array has a number of pieces:
    print("Lenght of the array: " + str(len(pieces)))

    # With four rotations, and four sides
    piece = random.randint(0, len(pieces))  # <- Piece
    rotation = random.randint(0, 3)  # <- Rotation
    side = random.randint(0, 3)  # <- Side

    print("\nSOLVING...")
    # We get the first piece (in one of her rotations)
    # It should start with 0, 0 and then another 2 sides
    first_piece = []

    # I create the solution array, "separated" by rows:
    solution_arr = [0] * length
    # I then find the first piece of the array and define the requirements
    oldPieces = pieces.copy()
    first_piece_remove, first_piece, requirements = find_first_piece_and_requirements(pieces, solution_arr)
    # print(requirements[int(width)])

    print("REQUIREMENTS: " + str(requirements))
    piecesIt = 1
    numberOfPieces = 0

    oldRequirements = requirements.copy()
    while piecesIt < length:
        if piecesIt == length-1:
            print("probando: " + str(pieces))
        for piece in pieces:
            # print("\n" + str(len(pieces)))
            # print(check_piece_number(piece[0]))
            numberOfPieces += 1

            if numberOfPieces > length:
                print("There isn't any valid piece to continue with. \nSolution not valid.\nTrying again...\n\n")
                solution_arr = [0] * length

                pieces = [None] * length
                pieces = oldPieces.copy()
                # print("\n" + str(len(pieces)))
                piecesIt = 1
                numberOfPieces = 0

                first_piece_remove, first_piece, requirements = find_first_piece_and_requirements(pieces, solution_arr)

                break

            for rot in piece:
                valid = True
                rot = str(rot)
                rot = rot.replace("[", "").replace("'", "").replace(",", "").replace("]", "").split(" ")
                tuple = list(map(list, zip(requirements[piecesIt], rot)))
                # print("Rot: " + str(rot))
                # print("Tuple: \n" + str(tuple[0][0]))
                for x in range(4):
                    # print("Tuple: " + str(tuple))
                    if tuple[x][0] != '*' and tuple[x][0] != tuple[x][1]:
                        # print("tuple[x][0] = " + tuple[x][0])
                        # print("tuple[x][1] = " + tuple[x][1])
                        # print(tuple[x][0] == tuple[x][1])
                        valid = False
                        break

                if valid:
                    # print("IS VALID: " + str(piecesIt))
                    # print("\nPiece[0]: " + str(piece[0]))
                    # print("Rot: " + rot)
                    print("Requirements: " + str(requirements[piecesIt]))
                    try:
                        requirements[piecesIt+1][0] = rot[2]
                        requirements[piecesIt+int(width)][1] = rot[3]
                        # print("New requirements: " + str(requirements[piecesIt+1]) + str(requirements[piecesIt+4]))
                    except:
                        print("Last row reached")
                    solution_arr[piecesIt] = check_piece_number(piece[0])
                    print("\nSolution ongoing like: \n" + str(solution_arr).replace("],", "\n").replace("[", " ")
                          .replace("]", "") + "\n")
                    print("Piece: " + str(piece))
                    numberOfPieces = 0
                    pieces.remove(piece)
                    piecesIt += 1
                    break

            if valid:
                break

    return solution_arr

def find_first_piece_and_requirements(pieces, solution_arr):
    # As far as I've understood, the solution wanted is the rotation that starts with the
    # lowest possible number (i.e: if the four corners are 1,2,3,4 - Then 1 is the preferred)
    # So I won't shuffle the array until I got the first corner

    # Note: Every corner must fit position 0 as they can be rotated

    for piece in pieces:
        for rot in piece:
            if rot[0] == '0' and rot[1] == '0':
                first_piece_remove = piece
                first_piece = rot

                # I randomize the array here, so we are not trying the same thing again and again
                numpy.random.shuffle(pieces)

                requirements = define_requirements(first_piece_remove, first_piece, pieces, solution_arr)
                return first_piece_remove, first_piece, requirements


def define_requirements(first_piece_remove, first_piece, pieces, solution_arr):
    print("First piece: " + str(first_piece))
    print("Piece number: " + str(check_piece_number(first_piece_remove[0])))
    pieces.remove(first_piece_remove)

    print("PIECES: " + str(pieces))

    # This could also be done with a 1D array, but this should make it
    # more legible
    solution_arr[0] = check_piece_number(first_piece_remove[0])

    # I set an array of restrictions, parallel to the one created for the pieces and solution
    requirements = []
    for i in enumerate(pieces):
        requirements = [['*'] * 4 for z in range(length)]  # edge requirements '*'=Any
        for req in range(0, length, int(height)):                   requirements[req][0] = '0'  # left side
        for req in range(0, int(height)):                           requirements[req][1] = '0'  # top side
        for req in range(int(height) - 1, length, int(height)):     requirements[req][2] = '0'  # right side
        for req in range(1, int(height) + 1):                       requirements[-req][3] = '0'  # bottom side

    requirements[1][0] = first_piece[2]
    requirements[int(width)][1] = first_piece[3]
    print("REQUIREMENTS: " + str(requirements))

    return requirements




def add_used_number(usednumbers, numbersaccepted):
    print("\n--Piece not valid--\n")
    usednumbers += 1
    print("Used numbers: " + str(usednumbers) + " --- Numbers left: " +
          str(len(numbersaccepted)))
    return usednumbers

def check_piece_number(piece):
    # pieceStr = str(piece).replace("[", "").replace("'", "").replace(",", "").replace("]", "")
    # print ("STRING: " + pieceStr)

    for i in range(0, 4):
        with open(filename, 'r') as fileToRead:
            line_number = 0

            rot = piece[i:] + piece[:i]
            rot = str(rot).replace("[", "").replace("'", "").replace(",", "").replace("]", "")

            # DEBUG: print("Rotation: " + rot)
            for line in fileToRead:
                line = line.replace("\n", "")
                # print("\nIs " + rot + " = " + line)
                # print(rot == line)
                if rot == line:
                    # print("Line Number: " + str(line_number))
                    return line_number
                line_number += 1

if __name__ == '__main__':
    print_hi('User')

    # First, I open and read the file
    filename = sys.argv[1]
    file = open(filename, "r")

    print("\nHere is the puzzle: \n" + file.read())

    height, width, array = create_array(filename)

    length = int(height) * int(width)



    # Then, I start to solve the puzzle
    solution_arr = solve(height, width, array)

    solution = str(solution_arr).replace("],", "\n").replace("[", " ").replace("]", "").replace(" ", "") \
        .split(",")
    print
    solution = "\n".join([" ".join(solution[i:i + int(width)]) for i in range(0, len(solution),
                                                                              int(width))])  # join into chunks of 4 and add a newline to separate the output
    print("\n" + str(solution) + "\n")
    # input("Press any key to close...")






