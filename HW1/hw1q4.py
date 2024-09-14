from itertools import product

import sys

def make_reverse_complement(input):
    complement = {'A': 'T', 'C': 'G', 'G': 'C', 'T': 'A'}

    reverse_complement = "".join(complement.get(base, base) for base in reversed(input))

    return reverse_complement

if len(sys.argv) != 3:
    print("Usage: python3 script.py <input_file> <output_file>")
    sys.exit(1)

# Assign the input and output filenames from command-line arguments
input_file = sys.argv[1] # First argument: input filename

output_file = sys.argv[2] # Second argument: output filename

# Read input from the file
with open(input_file, 'r') as in_file:
    # Read the first line, remove whitespace from both ends
    length = int(in_file.readline().strip())


total_list = []

if length >= 2:
    halves = ["".join(x) for x in list(product('ATGC',repeat=1))]
    total_list += [x + make_reverse_complement(x) for x in halves]

if length >= 4:
    halves = ["".join(x) for x in list(product('ATGC',repeat=2))]
    total_list += [x + make_reverse_complement(x) for x in halves]

if length >= 6:
    halves = ["".join(x) for x in list(product('ATGC',repeat=3))]
    total_list += [x + make_reverse_complement(x) for x in halves]

if length >= 8:
    halves = ["".join(x) for x in list(product('ATGC',repeat=4))]
    total_list += [x + make_reverse_complement(x) for x in halves]

total_list = sorted(total_list)

with open(output_file, 'w') as out_file:
    for item in total_list:
        out_file.writelines(item + "\n")
