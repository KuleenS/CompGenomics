import sys

def parse_fastq(fh):
    """ Parse reads from a FASTQ filehandle.  For each read, we
        return a name, nucleotide-string, quality-string triple. """
    
    read_index = 1

    file_lowest_quality = sys.maxsize
    file_lowest_quality_index = 1

    file_highest_quality = 0

    file_highest_quality_index = 1

    file_less_than_10s = 0

    file_greater_than_30s = 0

    file_other_characters = 0

    while True:
        first_line = fh.readline()
        if len(first_line) == 0:
            break  # end of file
        name = first_line[1:].rstrip()
        seq = fh.readline().rstrip()
        fh.readline()  # ignore line starting with +
        qual = fh.readline().rstrip()
        
        q_values = list(map(phred33_to_q, qual))

        total_quality = sum(q_values)

        if total_quality > file_highest_quality:
            file_highest_quality = total_quality

            file_highest_quality_index = read_index
        
        if total_quality < file_lowest_quality:

            file_lowest_quality = total_quality

            file_lowest_quality_index = read_index

        file_less_than_10s += len([x for x in q_values if x < 10])

        file_greater_than_30s += len([x for x in q_values if x >= 30])

        file_other_characters += len([x for x in seq if x not in "ACGT"])

        read_index += 1

    return f"{file_lowest_quality_index} {file_highest_quality_index} {file_less_than_10s} {file_greater_than_30s} {file_other_characters}"

def phred33_to_q(qual):
  """ Turn Phred+33 ASCII-encoded quality into Phred-scaled integer """
  return ord(qual)-33


if len(sys.argv) != 3:
    print("Usage: python3 script.py <input_file> <output_file>")
    sys.exit(1)
# Assign the input and output filenames from command-line arguments
input_file = sys.argv[1] # First argument: input filename
output_file = sys.argv[2] # Second argument: output filename
# Read input from the file
with open(input_file, 'r') as f:
    output = parse_fastq(f)
with open(output_file, 'w') as f:
    f.write(output)