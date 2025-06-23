import sys
from argparse import ArgumentParser, RawTextHelpFormatter
import os
import numpy as np
import re

def mkdir(path):
    if not os.path.exists(path):
        os.makedirs(path)

def generate_input(singles, doubles, input_paths):
    abort = False

    for input_path in input_paths:
        if os.path.exists(input_path):
            print(input_path + " already exists. Aborting.")
            abort = True

    if abort:
        exit(1)

    mkdir("inputs")

    for input_path in input_paths:
        with open(input_path, "w") as input_file:
            for item in singles:
                input_file.write(item + " - \n")
            for item in doubles:
                for ds in range(2):
                    input_file.write(item[ds] + " - \n")
    return 0


def parse_inputs(input_paths, singles, doubles):
    singles_results = np.zeros(shape=(len(singles), len(input_paths)), dtype=int)
    doubles_results = np.zeros(shape=(len(doubles), len(input_paths), 2), dtype=int)
   
    for person_id in range(len(input_paths)):
        with open(input_paths[person_id], "r") as input_file:

            # singles
            for s_id in range(len(singles)):
                line = input_file.readline()
                # check validity of line
                if not re.match("^" + singles[s_id] + r" - (\d|10|n|c|i)$", line):
                    print(input_paths[person_id] + ": line " + str(s_id + 1) + " not valid. Aborting.")
                    exit(3)
                else:
                    # write answer into array
                    response = line.split(" - ")[-1]
                    if response == "n\n":
                        response = -1
                    elif response == "c\n":
                        response = 11
                    elif response == "i\n":
                        response = 12
                    singles_results[s_id, person_id] = response

            # doubles
            for d_id in range(len(doubles)):
                for ds in range(2):
                    line = input_file.readline()
                    # check validity of line
                    if not re.match("^" + doubles[d_id][ds] + r" - (\d|10|n|c|i)$", line):
                        print(input_paths[person_id] + ": line " + str(len(singles) + d_id + 2) + " not valid. Aborting.")
                        exit(3)
                    else:
                        # write answer into array
                        response = line.split(" - ")[-1]
                        if response == "n\n":
                            response = -1
                        elif response == "c\n":
                            response = 11
                        elif response == "i\n":
                            response = 12
                        doubles_results[d_id, person_id, ds] = response
    return (singles_results, doubles_results)


def write_outputs(singles_results, doubles_results, persons, uncensored, singles, doubles):
    legend = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "c", "i", "n"]

    mkdir("outputs")

    # personal output
    for person_id in range(len(persons)):
        other_persons = persons[:]
        other_persons.remove(persons[person_id])

        with open("outputs/output_" + persons[person_id] + ".txt", "w") as output:
            output.write(f"{persons[person_id]}'s output file\n\nKink (your answer)")
            for other_person in other_persons:
                output.write(f" - {other_person}'s answer")
            output.write("\n\nSingles:\n")

            # singles
            for s_id in range(len(singles)):
                if singles_results[s_id, person_id] < 0 and not uncensored:
                    output.write(f"{singles[s_id]} (n)" + len(other_persons)*" - ###" + "\n")
                else:
                    output.write(f"{singles[s_id]} ({legend[singles_results[s_id, person_id]]})")
                    for other_person in other_persons:
                        output.write(f" - {legend[singles_results[s_id, persons.index(other_person)]]}")
                    output.write("\n")
            output.write("\nDoubles:\n")

            # doubles
            for d_id in range(len(doubles)):
                if uncensored:
                    output.write(f"{doubles[d_id][0]} | {doubles[d_id][1]} ({legend[doubles_results[d_id, person_id, 0]]}|{legend[doubles_results[d_id, person_id, 1]]})") 
                    for other_person in other_persons:
                        output.write(f" - {legend[doubles_results[d_id, persons.index(other_person), 0]]}|{legend[doubles_results[d_id, persons.index(other_person), 1]]}")
                    output.write("\n")
                else:
                    output.write(f"{doubles[d_id][0]} | {doubles[d_id][1]} ({legend[doubles_results[d_id, person_id, 0]]}|{legend[doubles_results[d_id, person_id, 1]]})")
                    
                    for other_person in other_persons:
                        if doubles_results[d_id, person_id, 1] < 0:
                            output.write(" - ###")
                        else:
                            output.write(f" - {legend[doubles_results[d_id, persons.index(other_person), 0]]}")
                        if doubles_results[d_id, person_id, 0] < 0:
                            output.write("|###")
                        else:
                            output.write(f"|{legend[doubles_results[d_id, persons.index(other_person), 1]]}")
 
                    output.write("\n")

    # common output
    with open("outputs/output_common.txt", "w") as output:
        output.write("Common output file\n\nKink")
        for person in persons:
            output.write(f" - {person}'s answer")
        output.write("\n\nSingles:\n")
        
        for s_id in range(len(singles)):
            if np.all(singles_results[s_id, :] >= 0) or uncensored:
                output.write(f"{singles[s_id]}")
                for person_id in range(len(persons)):
                    output.write(f" - {legend[singles_results[s_id, person_id]]}")
                output.write("\n")

        output.write("\nDoubles:\n")

        for d_id in range(len(doubles)):
            if len(persons) > 2: # (Censor everything if anyone said no)
                if np.all(doubles_results[d_id, :, :] >= 0) or uncensored:
                    output.write(f"{doubles[d_id][0]} | {doubles[d_id][1]}")
                    for person_id in range(len(persons)):
                        output.write(f" - {legend[doubles_results[d_id, person_id, 0]]}|{legend[doubles_results[d_id, person_id, 1]]}")

                    output.write("\n")
            else: # (Only censor the corresponding opposite of partner)
                if doubles_results[d_id, 0, 0] >= 0 and doubles_results[d_id, 1, 1] >= 0 or doubles_results[d_id, 0, 1] >= 0 and doubles_results[d_id, 1, 0] >= 0 or uncensored:
                    output.write(f"{doubles[d_id][0]} | {doubles[d_id][1]}")

                    for person_id in range(len(persons)):
                        if doubles_results[d_id, 0-person_id, 0] >= 0 and doubles_results[d_id, 1-person_id, 1] >= 0 or uncensored:
                            output.write(f" - {legend[doubles_results[d_id, person_id, 0]]}")
                        else:
                            output.write(" - ###")
                        if doubles_results[d_id, 1-person_id, 0] >= 0 and doubles_results[d_id, 0-person_id, 1] >= 0 or uncensored:
                            output.write(f"|{legend[doubles_results[d_id, person_id, 1]]}")
                        else:
                            output.write("|###")

                    output.write("\n")

    return 0


def main(raw_args):
    arg_parser = ArgumentParser("kinkcompare", description="A tool to compare kink preferences while not revealing that you like something to someone who doesn't. \nRank your preferences from 0 to 10, or use 'n' to fully exclude an item. By default, this will result in you not seeing your partner's response. 'c' can be used to denote curiousity and 'i' to denote indifference concerning an item.", formatter_class=RawTextHelpFormatter)

    arg_parser.add_argument("persons", metavar=("person"),  nargs="*", help="names of the persons to compare. (At least 2 unless -g is specified)")
    arg_parser.add_argument("-l", "--list", metavar="FILENAME", default="kinklist.txt", help="filename of kinklist to use. (default: kinklist.txt)")
    arg_parser.add_argument("-g", "--gen-input", action="store_true", help="generate input files to fill out, then exit.")
    arg_parser.add_argument("-u", "--uncensored", action="store_true", help="never censor partner's responses.")

    ARGS = arg_parser.parse_args(raw_args)

    if len(ARGS.persons) < 2 and not ARGS.gen_input:
        print("Please provide at least two persons to compare. (unless using -g) Aborting.")
        exit(4)

    with open(ARGS.list, "r") as kinklist:
        kinklist_lines = [item for item in kinklist.read().split("\n") if item != ""]

    singles = kinklist_lines[:kinklist_lines.index("#####")]
    doubles = [item.split(";") for item in kinklist_lines[kinklist_lines.index("#####")+1:]]

    input_paths = [f"inputs/input_{name}.txt" for name in ARGS.persons]

    if ARGS.gen_input:
        generate_input(singles, doubles, input_paths)
        exit(0)

    abort = False

    for input_path in input_paths:
        if not os.path.exists(input_path):
            print(input_path + " not found. Aborting.")
            abort = True

    if abort:
        exit(2)

    parsed_inputs = parse_inputs(input_paths, singles, doubles)

    write_outputs(parsed_inputs[0], parsed_inputs[1], ARGS.persons, ARGS.uncensored, singles, doubles)

    return 0


if __name__ == "__main__":
    args = sys.argv[1:]
    if len(args) == 0:
        args.append("-h")
    main(args)
