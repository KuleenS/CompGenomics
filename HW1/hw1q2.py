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
    input_string = in_file.read().strip()[::-1]

result = ""

for c in input_string:
    if c == "A":
        result += "T"
    elif c == "C":
        result += "G"
    elif c == "T":
        result += "A"
    elif c == "G":
        result += "C"
    
# Write the result to the output file
with open(output_file, 'w') as out_file:
    out_file.write(result)