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
    a = in_file.readline().strip()
    # Read the second line, remove whitespace from both ends
    b = in_file.readline().strip()
# Determine if the two strings are equal
# If they are, set result to ’Equal’, otherwise set it to ’Unequal’
result ='Equal' if a == b else 'Unequal'
# Write the result to the output file
with open(output_file, 'w') as out_file:
    out_file.write(result)