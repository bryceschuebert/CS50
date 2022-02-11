import csv
import sys


def main():

    # TODO: Check for command-line usage
    if len(sys.argv) != 3:
        sys.exit("Usage: python dna.py CSVFILENAME SEQUENCE")

    # TODO: Read database file into a variable
    csvFile = sys.argv[1]
    textFile = sys.argv[2]
    strData = []

    with open(csvFile) as data:
        reader = csv.DictReader(data)
        strHeader = reader.fieldnames[1:]
        for row in reader:
            strData.append(row)

    # TODO: Read DNA sequence file into a variable
    with open(textFile) as file:
        sequence = file.read()

    # TODO: Find longest match of each STR in DNA sequence
    counts = {}
    for subsequence in strHeader:
        counts[subsequence] = longest_match(sequence, subsequence)

    # TODO: Check database for matching profiles
    for person in strData:
        matches = 0
        for str in strHeader:
            if int(person[str]) != counts[str]:
                continue
            matches += 1

        if matches == len(strHeader):
            print(person["name"])
            exit(0)
    print("No match")
    exit(1)

    return


def longest_match(sequence, subsequence):
    """Returns length of longest run of subsequence in sequence."""

    # Initialize variables
    longest_run = 0
    subsequence_length = len(subsequence)
    sequence_length = len(sequence)

    # Check each character in sequence for most consecutive runs of subsequence
    for i in range(sequence_length):

        # Initialize count of consecutive runs
        count = 0

        # Check for a subsequence match in a "substring" (a subset of characters) within sequence
        # If a match, move substring to next potential match in sequence
        # Continue moving substring and checking for matches until out of consecutive matches
        while True:

            # Adjust substring start and end
            start = i + count * subsequence_length
            end = start + subsequence_length

            # If there is a match in the substring
            if sequence[start:end] == subsequence:
                count += 1

            # If there is no match in the substring
            else:
                break

        # Update most consecutive matches found
        longest_run = max(longest_run, count)

    # After checking for runs at each character in seqeuence, return longest run found
    return longest_run


main()
