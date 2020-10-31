import csv
import time

class Read:    
    def __init__(self, readStart, readLength):  # sets values of start and length when object is
        self.start = readStart                  # is constructed
        self.length = readLength
    
    def __lt__(self, other):     # needed to allow Read values to be sorted in a list
        return self.start < other.start

class Loci:   
    
    def __init__(self, readPosition):   # sets the value of the position of interest; coverage
        self.position = readPosition    # will keep count of Read values that overlap position
        self.coverage = 0               # and be incremented as such, so there is no need to
                                        # change the starting value from 0
    def __lt__(self, other):    # needed to allow sorting in list
        return self.position < other.position

def processReads(readFilePath, lociFilePath, outputFilePath):
# inputs: file paths
#       readFilePath: must have header as first row and two columns with integer values for each
#       lociFilePath: path to file containing values of interest, must have header as first row and two columns, seconds column may be empty
#       outputFilePath: output formatted the same as lociFilePath but with the second column filled in
# outputs: a new file is created according to outputFilePath with coverage data filled in
    reads_list = [] # to store read values from file
    loci_list = []  # to store loci values from file
    with open(readFilePath) as read_file:
        reads_reader = csv.reader(read_file, delimiter=',')
        next(reads_reader) # skip header row of file
        for row in reads_reader:   # loop to read in values from reads.csv and store in list
            input = Read(int(row[0]), int(row[1]))  # data read in as string must be explicitly converted to numeric type
            reads_list.append(input)
    # do the same thing with loci_list
    with open(lociFilePath) as loci_file:
        loci_reader = csv.reader(loci_file, delimiter=',')
        next(loci_reader)
        for row in loci_reader:
            input = Loci(int(row[0]))   # data read in as string must be explicitly converted to numeric type
            loci_list.append(input)

    # sort reads_list and loci_list - the values will be sorted in ascending order
    # based on Read.start and Loci.position respectively
    # being sorted will allow for for loci coverage to be determined systematically
    # since any Read objects with a start value higher than the Loci.position value of
    # concern will eliminate any further read values from affecting that loci, meaning
    # that the next loci can be processed without worry
    reads_list.sort()
    loci_list.sort()

    # process files by checking the start value of read vs respective loci's position -
    # once a loci position value is found that is less than read.start we know where the
    # next iteration of the loop can pick back up
    # note: the second while loop is to make sure whether there are further loci values that
    # may be included in the read's range;
    # i is declared outside the for loop so that the we can pick up where we left off

    i = 0
    earliestIndex = 0   # tracking index starts at 0
    for loci in loci_list:
        earliestFound = False
        i = earliestIndex    
        while (reads_list[i].start <= loci.position):
            if (reads_list[i].start + reads_list[i].length) > loci.position:   # already know value <= loci.position, must make sure adding length causes overlap
                loci.coverage += 1
                if earliestFound == False:  # save index of first match found for this loci for starting point for next loci
                    earliestIndex = i
                    earliestFound = True
            i += 1

    with open(outputFilePath, mode='w', newline='') as write_file:
        loci_writer = csv.writer(write_file, delimiter=',')
        loci_writer.writerow(['position', 'coverage'])
        for loci in loci_list:
            loci_writer.writerow([loci.position, loci.coverage])

before = time.time()
processReads('data\\reads.csv', 'data\\loci.csv', 'data\\loci.csv')

"""reads_list = [] # to store read values from file
loci_list = []  # to store loci values from file
with open('data\\reads.csv') as read_file:
    reads_reader = csv.reader(read_file, delimiter=',')
    next(reads_reader) # skip header row of file
    for row in reads_reader:   # loop to read in values from reads.csv and store in list
        input = Read(int(row[0]), int(row[1]))  # data read in as string must be explicitly converted to numeric type
        reads_list.append(input)
# do the same thing with loci_list
with open('data\\loci.csv') as loci_file:
    loci_reader = csv.reader(loci_file, delimiter=',')
    next(loci_reader)
    for row in loci_reader:
        input = Loci(int(row[0]))   # data read in as string must be explicitly converted to numeric type
        loci_list.append(input)"""

# sort reads_list and loci_list - the values will be sorted in ascending order
# based on Read.start and Loci.position respectively
# being sorted will allow for for loci coverage to be determined systematically
# since any Read objects with a start value higher than the Loci.position value of
# concern will eliminate any further read values from affecting that loci, meaning
# that the next loci can be processed without worry
"""reads_list.sort()
for read in reads_list:
    print([read.start, ', '])
loci_list.sort()

# process files by checking the start value of read vs respective loci's position -
# once a loci position value is found that is less than read.start we know where the
# next iteration of the loop can pick back up
# note: the second while loop is to make sure whether there are further loci values that
# may be included in the read's range;
# i is declared outside the for loop so that the we can pick up where we left off

i = 0
earliestIndex = 0   # tracking index starts at 0
for loci in loci_list:
    earliestFound = False
    i = earliestIndex    
    while (reads_list[i].start <= loci.position):
        if (reads_list[i].start + reads_list[i].length) > loci.position:   # already know value <= loci.position, must make sure adding length causes overlap
            loci.coverage += 1
            if earliestFound == False:  # save index of first match found for this loci for starting point for next loci
                earliestIndex = i
                earliestFound = True
        i += 1

with open('data\\loci.csv', mode='w', newline='') as write_file:
    loci_writer = csv.writer(write_file, delimiter=',')
    loci_writer.writerow(['position', 'coverage'])
    for loci in loci_list:
        loci_writer.writerow([loci.position, loci.coverage])"""

after = time.time()
elapsed = after - before
print(elapsed, "seconds elapsed")
    
    
