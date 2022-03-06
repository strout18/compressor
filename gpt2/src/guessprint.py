import sys, os, csv
from gpt2.src import ics_api as ics
import regex as re
from gpt2.src import intermediateencoding as ie

window = 8
TOP_K = 40


# splits array according to decided standards - talk about this in thesis?
def cleansplit(txtstr):
    pat = re.compile(r"""'s|'t|'re|'ve|'m|'ll|\n|'d| ?\p{L}+| ?\p{N}+| ?[^\s\p{L}\p{N}]+|\s+(?!\S)|\s+""") # from encoder.py
    return re.findall(pat, txtstr)

# NOTE : test file that ends in new line

# args = infile, window
def write_guess(argv):
    # global total_encoding, incorrect, guessct, compressed, total
    #reset globals
    global window, TOP_K

    infile = argv[0]    # file name
    # should prob error check command line args
    guessfile = infile + ".guess"  # file name
    with open(infile, 'r') as inf:
        with open(guessfile, 'w') as guessf:
            ftxt = inf.read()
            #print("Writing window")
            #print ("Encoding now " + total_encoding)
            splat = cleansplit(ftxt)
            print(splat)
            for ct, wd in enumerate(splat):  
                prev = ics.slice_window(int(window), splat, ct) #preceding text
                if prev:
                    guess = ics.run_model(prev, length=1, top_k=int(TOP_K))
                    guessf.write("PREV " + prev)
                    guessf.write("TARGET " + wd)
                    guessf.write("GUESS " + guess)
                    # print ("The guess is " + guess)
                if prev and guess == wd:
                    # print ("Guess was correct")
                    guessf.write("CORRECT")
                else:
                    guessf.write("INCORRECT")

    


if __name__ == "__main__":
    write_guess(sys.argv[1:])
