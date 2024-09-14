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
    print("Usage: python3 script.py <fasta_file> <fastq_file> <output_file>")
    sys.exit(1)
# Assign the input and output filenames from command-line arguments
fasta_file = sys.argv[1] 
fastq_file = sys.argv[2] 
output_file = sys.argv[3]


with open(fasta_file, 'r') as f:
    header = f.readline()

    input_string = "".join(f.readlines())

    reference_genome = "".join(x for x in input_string if x in "ACTG")

index = IndexHash(reference_genome, 6)

total_matches = 0

max_length = len(max(index.index.values(), key=lambda x: len(x)))

max_hitters = []

for item in index.index:
    if len(index.index[item]) == max_length:
        max_hitters.append(item)
    
read_max_matches = 0
read_max_matches_min_offset = 0

with open(fastq_file, 'r') as fh:
    while True:
        first_line = fh.readline()
        if len(first_line) == 0:
            break  # end of file
        name = first_line[1:].rstrip()
        seq = fh.readline().rstrip()
        fh.readline()  # ignore line starting with +
        qual = fh.readline().rstrip()

        query_pattern = seq[:6]

        offsets = index.query(query_pattern)

        match_offsets = []

        for offset in offsets:

            if seq[6:] == reference_genome[offset+6:offset+len(seq)]:
                total_matches += 1
                match_offsets.append(offset)
        
        if len(match_offsets) >= read_max_matches:
            read_max_matches = len(match_offsets)

            read_max_matches_min_offset = min(read_max_matches_min_offset, min(match_offsets))

print(f"{','.join(sorted(max_hitters))} {total_matches} {read_max_matches_min_offset}")

with open(output_file, "w") as f:
    f.write(f"{','.join(sorted(max_hitters))} {total_matches} {read_max_matches_min_offset}")