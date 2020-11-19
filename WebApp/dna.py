from sys import argv
import csv


def dna_main(db_file, seq_file):
    
    # Variable to track current row
    row_count = 1
    nstr = 0

    with open(db_file) as database_file:
        df = csv.reader(database_file)

        for row in df:
            if row_count == 1:
                # No of strs in the given csv files
                nstr = len(row) - 1

                # List for storing max STR count for each STR's corresponding index
                str_max = []

                # Calculating the max occurence of a particular STR (in every iteration max count for an STR with corresponding index i is calculated)
                for i in range(nstr):
                    # Initialising STR max counts to zero
                    str_max.append(0)

                    # Opening the sequence file given
                    with open(seq_file) as seq:
                        seqf = seq.read()

                        # Current reouccring count
                        count = 0
                        # Flag to see if we are in reoccuring STR part of the file
                        flag = 1
                        j = 0
                        while j < len(seqf):
                            lenstr = len(row[i + 1])
                            if seqf[j:j + lenstr] == row[i + 1]:
                                count += 1
                                j += lenstr
                                flag = 1
                            # Flag set to 0 if not in the part of file with reoccuring STR
                            else:
                                flag = 0
                                j += 1

                            if count > str_max[i]:
                                str_max[i] = count

                            if flag == 0:
                                count = 0

                row_count += 1
            else:
                # Checking if the calculated STR max count form seq is equal to any of the member's STR counts
                equal_count = 0
                for i in range(nstr):
                    if int(row[i + 1]) == str_max[i]:
                        equal_count += 1

                if equal_count == nstr:
                    print(row[0])
                    return row[0]

    print("No Match")
    return "No Match"