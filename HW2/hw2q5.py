import sys

def hamming_distance(str1, str2):
    return sum(c1 != c2 for c1, c2 in zip(str1, str2))

def phred33_to_q(qual):
    """ Turn Phred+33 ASCII-encoded quality into Phred-scaled integer """
    return ord(qual)-33

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

matches = set()

with open(fastq_file, 'r') as fh, open(output_file ,"w") as out:
    while True:
        first_line = fh.readline()
        if len(first_line) == 0:
            break  # end of file
        name = first_line[1:].rstrip()
        seq = fh.readline().rstrip()
        fh.readline()  # ignore line starting with +
        qual = fh.readline().rstrip()

        partitions = parts = [seq[i:i+6] for i in range(0, len(seq), 6)]

        offsets_batches = [index.query(partition) for partition in partitions]

        index_hits = [len(offsets_batch) for offsets_batch in offsets_batches]

        mismatch_offsets = {0: [], 1: [], 2: [] , 3:[] , 4: []}

        for offsets_batch, offset_location in zip(offsets_batches, range(0, len(seq), 6)):

            characters_before_offset = offset_location

            characters_after_offset = len(seq)-offset_location

            for offset in offsets_batch:
                reference_genome_location_r = offset- offset_location
                reference_genome_location_l = offset + characters_after_offset
                if reference_genome_location_r >= 0 and reference_genome_location_l <= len(reference_genome):
                    distance = hamming_distance(seq, reference_genome[reference_genome_location_r:reference_genome_location_l])

                    if distance <= 4:
                        matches.add((seq, qual, reference_genome_location_r, reference_genome_location_l))

matches = list(matches)

for i in range(len(reference_genome)):

    base_qualities = {"A": 0, "C": 0, "G": 0, "T": 0}

    for match in matches:
        if i>= match[2] and i < match[3] and match[0][i-match[2]] != reference_genome[i]:
            base_quality = phred33_to_q(match[1][i-match[2]])

            if match[0][i-match[2]] in base_qualities:
                base_qualities[match[0][i-match[2]]] += base_quality

    max_number = second_max_number = 0
    max_ref = second_max_ref = ""
    
    for key, num in base_qualities.items():
        if num > max_number:
            second_max_number = max_number
            max_number = num
            max_ref = key
        elif num > second_max_number and num != max_number:
            second_max_number = num
            second_max_ref = key
    
    if max_number > 20:
        if max_number == second_max_number:
            if max_ref > second_max_ref:
                print(i, reference_genome[i], second_max_ref, second_max_number, max_ref, max_number)
            else:
                print(i, reference_genome[i], max_ref, max_number, second_max_ref, second_max_number)

        else:
            print(i, reference_genome[i], max_ref, max_number, "-" if second_max_number <= 20 else second_max_ref, 0 if second_max_number <= 20 else second_max_number)