import sys
from gpt2.src import intermediateencoding as ie
def transform(argv):
    intermfile = argv[0]
    transintermfile = argv[1]
    with open(intermfile, 'r') as inf:
        ftxt = inf.read()
        numbers, incorrect = ftxt.split('\n', 1)
        numpointer = 0
        newnums = ""
        curr_inc = True
        while numpointer < len(numbers):
            if curr_inc:
                numpointer += 2 # skip 0,
                len_cutoff = numbers.index(',', numpointer)
                sliced_inc = numbers[numpointer:len_cutoff + 1]
                newnums += sliced_inc
                curr_inc = False
                numpointer += len(sliced_inc)
            else:
                guess_cutoff = numbers.index(',', numpointer)
                sliced_corr = numbers[numpointer:guess_cutoff + 1]
                newnums += sliced_corr
                numpointer += len(sliced_corr)
                curr_inc = True
    # with open(transintermfile, 'w') as outf:
    total_encoding = newnums + "\n" + incorrect
    ie.crunch_bz2(total_encoding, transintermfile)
        # outf.write(newnums + "\n" + incorrect)

if __name__ == "__main__":
    transform(sys.argv[1:])