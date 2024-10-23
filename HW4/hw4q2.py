import sys

def make_kmer_table(seqs, k):
    """ Given read dictionary and integer k, return a dictionary that
    maps each k-mer to the set of names of reads containing the k-mer. """
    table = {}
    for name, seq in seqs.items():
        for i in range(0, len(seq) - k + 1):
            kmer = seq[i:i+k]
            if kmer not in table:
                table[kmer] = set()
            table[kmer].add(name)
    return table

def suffix_prefix_match(str1, str2, min_overlap):
    if len(str2) < min_overlap:
        return 0
    str2_prefix = str2[:min_overlap]
    str1_pos = -1
    while True:
        str1_pos = str1.find(str2_prefix, str1_pos + 1)
        if str1_pos == -1:
            return 0
        str1_suffix = str1[str1_pos:]
        if str2.startswith(str1_suffix):
            return len(str1_suffix)


if len(sys.argv) != 4:
    print("Usage: python3 script.py <fastq_file> <k_file> <output_file>")
    sys.exit(1)
# Assign the input and output filenames from command-line arguments
fastq_file = sys.argv[1] 
k = int(sys.argv[2])
output_file = sys.argv[3]

fastq_data = dict()

with open(fastq_file, 'r') as fh:
    while True:
        first_line = fh.readline()
        if len(first_line) == 0:
            break  # end of file
        name = first_line[1:].rstrip()
        seq = fh.readline().rstrip()
        fh.readline()  # ignore line starting with +
        qual = fh.readline().rstrip()

        fastq_data[name] = seq

seq_table = make_kmer_table(fastq_data, k)


total_scores = []

for name,seq in fastq_data.items():
    scores = []

    seqs_to_test = set()

    for i in range(0, len(seq) - k + 1):
        seqs_to_test |= seq_table[seq[i:i+k]]

    for seq_to_test in seqs_to_test:
        if seq_to_test != name:
            scores.append((suffix_prefix_match(seq, fastq_data[seq_to_test], k), seq_to_test))

    if len(scores) > 0:
        scores = sorted(scores, key=lambda x: x[0], reverse=True)

        if scores[0][0] > 0:
            if len(scores) == 1:
                total_scores.append((name,scores[0][0],scores[0][1]))
            elif len(scores) > 1 and scores[1][0] != scores[0][0]:
                total_scores.append((name,scores[0][0],scores[0][1]))

total_scores = sorted(total_scores, key=lambda x: x[0])

with open(output_file, "w") as f:
    for total_score in total_scores:
        f.write(f"{total_score[0]} {total_score[1]} {total_score[2]}\n")