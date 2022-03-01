import sys
from gpt2.src import ics_api as ics
import regex as re
from gpt2.src import intermediateencoding as ie
 

window = 8
TOP_K = 40

def gpt_decode(argv):
    global window, TOP_K
    total_decoding = ""
    infile = argv[0]    # file name
    # window = int(argv[1])    # do error checking
    outfile = infile + ".plaintext"  # file name
    ftxt = ie.uncrunch_bz2(infile)
    # with open(infile, 'r') as inf:
    #     ftxt = inf.read()
    # print (ftxt)
    # print ("reading window as " + str(window))
    numpointer = 0
    tkpointer = 0
    encodingsplit = ftxt.find('\n') # division between numbers and incorrect
    numbers = ftxt[:encodingsplit]
    incorrect = ftxt[encodingsplit+1:]
    print ("numbers are ")
    print (numbers)
    print ("incorrect")
    print (incorrect)
    while numpointer < len(numbers):
        guess_cutoff = numbers.index(',', numpointer)
        guessc = numbers[numpointer:guess_cutoff]
        guesslen = len(guessc)
        if int(guessc) == 0:
            print("Guess char was 0")
            numpointer += guesslen + 1
            len_cutoff = numbers.index(',', numpointer)
            lenchars = numbers[numpointer:len_cutoff]
            print ("lenchars are " + lenchars)
            txtlen = int(lenchars)    # gives num of chars in current chunk of unguessed text
            print("txtlen " + str(txtlen))
            numpointer += len(lenchars) + 1
            txtchars = incorrect[tkpointer:tkpointer+txtlen]    # chunk of unguessed text
            print("decoded as " + txtchars)
            total_decoding += txtchars
            tkpointer += txtlen
        else:
            print ("Guess char was " + guessc)
            pat = re.compile(r"""'s|'t|'re|'ve|'m|'ll|\n|'d| ?\p{L}+| ?\p{N}+| ?[^\s\p{L}\p{N}]+|\s+(?!\S)|\s+""") # from encoder.py
            for _ in range(int(guessc)):
                decoding_arr = re.findall(pat, total_decoding)
                print ("decoding arr " + str(decoding_arr))
                prev = ics.slice_window(window, decoding_arr, len(decoding_arr))
                print ("Running with prev " + prev)
                guess = ics.run_model(prev, length=1, top_k=int(TOP_K))
                print ("Guess is " + guess)
                total_decoding += guess
                # print ("Total decoding now " + total_decoding)
            numpointer += guesslen + 1 # push pointer to next section, comma
    print (total_decoding)
    with open(outfile, 'w') as outf:
        outf.write(total_decoding)


if __name__ == "__main__":
    gpt_decode(sys.argv[1:])