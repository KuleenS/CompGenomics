import sys

def hamming_distance(str1, str2):
    return sum(c1 != c2 for c1, c2 in zip(str1, str2))

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

                    if distance in mismatch_offsets:
                        mismatch_offsets[distance].append(reference_genome_location_r)

        mismatch_str = ""

        for item in mismatch_offsets:

            mismatch_str += f"{item}:"

            if len(mismatch_offsets[item]) != 0:
                mismatch_str += ",".join([str(x) for x in set(mismatch_offsets[item])])
            
            mismatch_str += " "
        
        total_str = f'{" ".join([str(x) for x in index_hits])} {mismatch_str}'

        print(total_str)
    
        out.write(f'{total_str}\n')
            