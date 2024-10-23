import sys

from collections import defaultdict

if len(sys.argv) != 3:
    print("Usage: python3 script.py <input_file> <output_file>")
    sys.exit(1)
# Assign the input and output filenames from command-line arguments
input_file = sys.argv[1] 
output_file = sys.argv[2]

with open(input_file) as f:
    data = [x.strip().split(" ") for x in f.readlines()]

unitig_left_graph = defaultdict(list)
unitig_right_graph = defaultdict(list)

for line in data:
    unitig_left_graph[line[2]].append((line[0], int(line[1])))
    unitig_right_graph[line[0]].append((line[2], int(line[1])))

BMR = dict()
BML = dict()

for key in unitig_left_graph:
    BML[key] = max(unitig_left_graph[key], key=lambda x: x[1])

for key in unitig_right_graph:
    BMR[key] = max(unitig_right_graph[key], key=lambda x: x[1])

seen_reads = set()

unitigs = []

for key in BML:

    if key in seen_reads:
        continue

    left_unitig  = []

    pointer = key

    while pointer in BML:
        next_pointer = BML[pointer][0]

        if BMR[next_pointer][0] == pointer:
            pointer_value = BML[pointer][1]
            left_unitig.append((pointer, pointer_value))
            pointer = next_pointer 
            seen_reads.add(pointer)
        else:
            break
    
    if pointer not in BML:
        left_unitig.append((pointer, pointer_value))
    
    pointer = key

    right_unitig = []

    while pointer in BMR:
        next_pointer = BMR[pointer][0]

        if BML[next_pointer][0] == pointer:
            pointer_value = BMR[pointer][1]
            right_unitig.append((pointer, pointer_value))
            pointer = next_pointer 
            seen_reads.add(pointer)
        else:
            break
    
    if pointer not in BMR and any([x[0] == pointer for x in right_unitig]):
        right_unitig.append((pointer, pointer_value))
    
    unitigs.append((right_unitig+left_unitig)[::-1])

unitigs = sorted(unitigs, key=lambda x: x[0][0])

with open(output_file, "w") as f:
    for unitig in unitigs:
        for i, read in enumerate(unitig):
            if i == 0:
                f.write(f"{read[0]}\n")
            else:
                f.write(f"{read[1]} {read[0]}\n")