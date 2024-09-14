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

result = ""

for i, c in enumerate(input_string):
    if c == "A":
        result += "A"
    elif c == "C":
        result += "C"
    elif c == "T":
        result += "U"
    elif c == "G":
        result += "G"

result = '-'.join(result[i:i+3] for i in range(0, len(result), 3))
    
# Write the result to the output file
with open(output_file, 'w') as out_file:
    out_file.write(result)