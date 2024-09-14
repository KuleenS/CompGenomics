import sys

if len(sys.argv) != 3:
    print("Usage: python3 script.py <input_file> <output_file>")
    sys.exit(1)
# Assign the input and output filenames from command-line arguments
input_file = sys.argv[1] # First argument: input filename
output_file = sys.argv[2] # Second argument: output filename
# Read input from the file
with open(input_file, 'r') as in_file:
    # Read the first line, remove whitespace from both ends
    input_string = in_file.read().strip()

inverse_map = {'A': 'GCC',
 'C': 'UGC',
 'D': 'GAC',
 'E': 'GAG',
 'F': 'UUC',
 'G': 'GGC',
 'H': 'CAC',
 'I': 'AUC',
 'K': 'AAG',
 'L': 'CUC',
 'M': 'AUG',
 'N': 'AAC',
 'P': 'CCC',
 'Q': 'CAG',
 'R': 'CGC',
 'S': 'AGC',
 'T': 'ACC',
 'V': 'GUC',
 'W': 'UGG',
 'Y': 'UAC'}

output = ""

for c in input_string:
    if c in inverse_map:
        output += inverse_map[c]

# Write the result to the output file
with open(output_file, 'w') as out_file:
    out_file.write(output)