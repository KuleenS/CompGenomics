import sys
from collections import defaultdict

codon_to_protein = {"GCU":"A",
"GCC":"A",
"GCA":"A",
"GCG":"A",
"UGU":"C",
"UGC":"C",
"GAU":"D",
"GAC":"D",
"GAA":"E",
"GAG":"E",
"UUU":"F",
"UUC":"F",
"GGU":"G",
"GGC":"G",
"GGA":"G",
"GGG":"G",
"CAU":"H",
"CAC":"H",
"AUU":"I",
"AUC":"I",
"AUA":"I",
"AAA":"K",
"AAG":"K",
"UUA":"L",
"UUG":"L",
"CUU":"L",
"CUC":"L",
"CUA":"L",
"CUG":"L",
"AUG":"M",
"AAU":"N",
"AAC":"N",
"CCU":"P",
"CCC":"P",
"CCA":"P",
"CCG":"P",
"CAA":"Q",
"CAG":"Q",
"CGU":"R",
"CGC":"R",
"CGA":"R",
"CGG":"R",
"AGA":"R",
"AGG":"R",
"UCU":"S",
"UCC":"S",
"UCA":"S",
"UCG":"S",
"AGU":"S",
"AGC":"S",
"ACU":"T",
"ACC":"T",
"ACA":"T",
"ACG":"T",
"GUU":"V",
"GUC":"V",
"GUA":"V",
"GUG":"V",
"UGG":"W",
"UAU":"Y",
"UAC":"Y"}

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

cleaned_input_string = ""

for c in input_string:
    if c in 'ACTGU':
        cleaned_input_string += c

count_dict = {x: 0 for x in codon_to_protein.values()}

for i in range(0, len(cleaned_input_string), 3):
    if cleaned_input_string[i:i+3] in codon_to_protein:
        count_dict[codon_to_protein[cleaned_input_string[i:i+3]]] += 1

result = ",".join([str(x) for x in count_dict.values()])

with open(output_file, 'w') as out_file:
    out_file.write(result)
    
