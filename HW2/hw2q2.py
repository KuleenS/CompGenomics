import sys

class IndexHash:
    
    def __init__(self, t: str, ln: int):
        """ Create index, extracting substrings of length 'ln' """
        self.t = t
        self.ln = ln
        self.index = dict()
        for i in range(len(t)-ln+1):
            substr = t[i:i+ln]
            if substr in self.index:
                self.index[substr].append(i) # substring already in dictionary
            else:
                self.index[substr] = [i] # add to dictionary
    
    def __len__(self):
        return len(self.index)

    def query(self, p):
        """ Return candidate alignments for p """
        return self.index.get(p[:self.ln], [])[:]

if len(sys.argv) != 4:
    print("Usage: python3 script.py <fasta_file> <k_file> <output_file>")
    sys.exit(1)
# Assign the input and output filenames from command-line arguments
fasta_file = sys.argv[1] 
k_file = sys.argv[2] 
output_file = sys.argv[3]

with open(k_file, 'r') as in_file:
    # Read the first line, remove whitespace from both ends
    k = int(in_file.readline().strip())

with open(fasta_file, 'r') as f:
    header = f.readline()

    input_string = "".join(f.readlines())

    cleaned_input_string = "".join(x for x in input_string if x in "ACTG")

index = IndexHash(t=cleaned_input_string, ln=k)

exactly_one_keys = 0

for item in index.index:
    if len(index.index[item]) == 1:
        exactly_one_keys += 1

with open(output_file, "w") as f:
    f.write(f"{len(index)} {exactly_one_keys}")