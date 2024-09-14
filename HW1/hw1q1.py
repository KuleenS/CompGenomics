# Import the sys module to access command-line arguments
import sys
# This module is for your reference to understand the usage
if len(sys.argv) != 3:
    print("Usage: python3 hw1q1b.py <input_file> <output_file>")
    sys.exit(1)
# Assign the input and output filenames from command-line arguments
input_file = sys.argv[1] # First argument: input filename
output_file = sys.argv[2] # Second argument: output filename
# Open both input and output files - input file for reading and output file for writing
with open(input_file, 'r') as in_file, open(output_file, 'w') as out_file:
    # Iterate through each line in the input file
    for line in in_file:
        # Iterate through each character in the line
        for c in line:
            # Check if the character is one of ’A’, ’C’, ’G’, or ’T’
            if c in 'ACGT':
                # If so, write it 
                out_file.write(c)