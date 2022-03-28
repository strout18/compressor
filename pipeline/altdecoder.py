from transformers import pipeline
import sys
from pipeline import intermediateencoding as ie
from pipeline import window as utils
 

# window = 8
# TOP_K = 40

def pipeline_decode(argv):
    # global window, TOP_K
    total_decoding = ""
    infile = argv[0]    # file name
    modelname = argv[1]
    window = argv[2]
    # window = int(argv[1])    # do error checking
    outfile = infile + ".plaintext"  # file name
    tkzer = utils.get_tkzer(modelname)
    ftxt = ie.uncrunch_bz2(infile)
    # with open(infile, 'r') as inf:
    #     ftxt = inf.read()
    # print (ftxt)
    # print ("reading window as " + str(window))
    numpointer = 0
    tkpointer = 0
    mask_token = tkzer.mask_token
    unmasker = pipeline('fill-mask', model=modelname)
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
            for _ in range(int(guessc)):
                decoding_arr = tkzer.tokenize(total_decoding)
                print ("decoding arr " + str(decoding_arr))
                prev = utils.slice_window(window, decoding_arr, len(decoding_arr), tkzer)
                print ("Running with prev " + prev)
                guess = unmasker(prev + f"{mask_token}")[0]["token_str"]
                print ("Guess is " + guess)
                total_decoding += guess
                # print ("Total decoding now " + total_decoding)
            numpointer += guesslen + 1 # push pointer to next section, comma
    print (total_decoding)
    with open(outfile, 'w') as outf:
        outf.write(total_decoding)


if __name__ == "__main__":
    pipeline_decode(sys.argv[1:])