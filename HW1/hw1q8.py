from collections import defaultdict
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
    input_string = in_file.readline().strip()

count_dict = dict()

for i in range(0, len(input_string)-5):

    window = input_string[i:i+6]

    if input_string[i:i+6] not in count_dict:
        count_dict[window] = [i]
    else:
        count_dict[window].append(i)

m = len(max(count_dict.values(), key=lambda x: len(x)))

lexiographic_minimum = min([x[0] for x in count_dict.items() if len(x[1]) == m])

with open(output_file, 'w') as out_file:
    out_file.write(",".join([str(x) for x in count_dict[lexiographic_minimum]]))
    
