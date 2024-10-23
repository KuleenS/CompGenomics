from numpy import zeros
import sys

def exampleCost(xc, yc):
    if xc == yc: 
        return 1 # match
    else:
        return 0

def globalAlignment(x, y, s):
    """ Calculate global alignment value of sequences x and y using
        dynamic programming.  Return global alignment value. """
    D = zeros((len(x)+1, len(y)+1), dtype=int)
    for j in range(1, len(y)+1):
        D[0, j] = D[0, j-1] + s('-', y[j-1])
    for i in range(1, len(x)+1):
        D[i, 0] = D[i-1, 0] + s(x[i-1], '-')
    for i in range(1, len(x)+1):
        for j in range(1, len(y)+1):
            D[i, j] = max(D[i-1, j-1] + s(x[i-1], y[j-1]), # diagonal
                          D[i-1, j  ] + s(x[i-1], '-'),    # vertical
                          D[i  , j-1] + s('-',    y[j-1])) # horizontal
    return D, D[len(x), len(y)]


if len(sys.argv) != 3:
    print("Usage: python3 script.py <input_file> <output_file>")
    sys.exit(1)
# Assign the input and output filenames from command-line arguments
input_file = sys.argv[1] 
output_file = sys.argv[2]

with open(input_file, 'r') as in_file:
    # Read the first line, remove whitespace from both ends
    x = in_file.readline().strip()
    # Read the second line, remove whitespace from both ends
    y = in_file.readline().strip()

matrix, score = globalAlignment(x,y,exampleCost)

with open(output_file, "w") as f:
    f.write(str(score))