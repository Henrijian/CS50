from sys import argv
import os
import csv

NAME_COL = "name"


def main(args):
    if len(args) != 3:
        print("Usage: python dna.py data.csv sequence.txt")
        return
    data_path = args[1]
    # Get set of all STRs from data file
    STRs = get_STR_set(data_path)
    # Get dict of individuals count of STRs
    # keys = [name, STRs]
    data_dict = get_data_dict(data_path)

    sequence_path = args[2]
    # Get dict of specified STRs count
    sequence_dict = get_STR_dict(sequence_path, STRs)
    # Find owner of sequence dict in data dict
    sequence_owner = find_sequence_owner(sequence_dict, data_dict)
    if sequence_owner != "":
        print(sequence_owner)
    else:
        print("No match")
    return

# Get all STRs from data file


def get_STR_set(data_path):
    result = set()
    if os.path.isfile(data_path):
        with open(data_path, newline="") as data_file:
            reader = csv.reader(data_file, delimiter=",")
            for row in reader:
                result = set(row)
                result.discard(NAME_COL)
                break
    return result

# Get dict of individuals count of STRs
# keys = [name, STRs]


def get_data_dict(data_path):
    result = dict()
    if os.path.isfile(data_path):
        with open(data_path, newline='') as data_file:
            reader = csv.DictReader(data_file)
            for row in reader:
                for key in row:
                    if key in result:
                        result[key].append(row[key])
                    else:
                        result[key] = [row[key]]
    return result

# Get dict of specified STRs count


def get_STR_dict(sequence_path, STRs):
    result = dict()
    for STR in STRs:
        result[STR] = 0
    dna_sequence = str()
    if os.path.isfile(sequence_path):
        sequence_file = open(sequence_path, "r")
        for line in sequence_file:
            dna_sequence += line
    for STR in STRs:
        consecutive_count = 1
        found_idx = dna_sequence.find(STR * consecutive_count)
        while found_idx != -1:
            result[STR] = consecutive_count
            consecutive_count += 1
            found_idx = dna_sequence.find(STR * consecutive_count)
    return result

# Find owner of sequence dict in data dict


def find_sequence_owner(sequence_dict, data_dict):
    result = str()
    if NAME_COL in data_dict:
        for i, name in enumerate(data_dict[NAME_COL]):
            STR_match = True
            for STR in sequence_dict:
                if STR in data_dict:
                    if str(sequence_dict[STR]) != str(data_dict[STR][i]):
                        STR_match = False
                        break
                else:
                    STR_match = False
                    break
            if STR_match:
                result = name
                break
    return result


if __name__ == "__main__":
    main(argv)