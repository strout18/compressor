from transformers import pipeline
import os, sys, csv
from pipeline import intermediateencoding as ie # make sure it's not confused
from pipeline import window as utils

# TO DO DECIDE TOP K
statfile = "slurpstats.txt"
TOP_K = 5
declare_length = True


def on_correct(curr_incorrect, numbers):
    global declare_length
    # dump the buffer of incorrects into encoding
    if declare_length:
        txt = '0,'
        txt += str(len(curr_incorrect)) + ","
        print("curr_incorrect is " + curr_incorrect)
        print ("Length of incorrect is " + str(len(curr_incorrect)))
        print ("Str with guess and len: " + txt)
        numbers += txt
        declare_length = False
        curr_incorrect = ""
        # print ("Extending from incorrect. Total encoding is now " + total_encoding)
    return curr_incorrect, numbers

def on_incorrect(guessct, numbers):
    # how much to pad to?
    global declare_length
    declare_length = True
    if guessct > 0:
        if guessct > 1:
            numbers += str(guessct) + ","
        # print ("Total encoding now " + total_encoding)
        guessct = 0
    return guessct, numbers

# args = infile, window
def pipeline_encode(argv):
    # global total_encoding, incorrect, guessct, compressed, total
    #reset globals
    # global window, TOP_K
    numbers = ""
    incorrect = ""
    guessct = 0
    compressed = 0
    total = 0
    curr_incorrect = ""
    correctbuffer = ""

    infile = argv[0]    # file name 
    modelname = argv[1]
    window = argv[2]
    # should prob error check command line args
    out_intermfile = infile + ".interm"  # file name
    unmasker = pipeline('fill-mask', model=modelname)
    with open(infile, 'r') as inf:
        ftxt = inf.read()
        #print("Writing window")
        #print ("Encoding now " + total_encoding)
        tkzer = utils.get_tkzer(modelname)
        splat = tkzer.tokenize(ftxt)
        # print(splat)
        for ct, tk in enumerate(splat):  
            prev = utils.slice_window(int(window), splat, ct, tkzer) #preceding text
            # print("#" * 40)
            # print("Calling extend_encoding on wd \"" + wd + "\" with prev \"" + prev)
            # global guessct, incorrect, total, compressed
            # print ("The current word is " + wd + "and the previous word is " + prev)
            if prev:
                guess = unmasker(prev + f"{tkzer.mask_token}")[0]["token_str"]
                # print ("The guess is " + guess)
            if prev and guess == tkzer.convert_tokens_to_string([tk]):
                # print ("Guess was correct")
                guessct += 1
                compressed += 1
                if guessct == 1:    # slurp unless guessct >= 2
                    correctbuffer += guess
                    print ("adding to cbuff")
                else:
                    correctbuffer = ""
                    # print ("Guesscount " + str(guessct))
                    # print ("Dumping incorrect")
                    # print (incorrect)
                    print("Dumping incorrect, guess was correct")
                    curr_incorrect, numbers = on_correct(curr_incorrect, numbers)  # clear out incorrect buffer before logging correct
                    print ("numbers is now " + numbers)
            else:
                print ("Guess was incorrect")
                # print ("Guess count:" + str(guessct))
                print ("Dumping correct")
                guessct, numbers = on_incorrect(guessct, numbers)
                if correctbuffer:
                    incorrect += correctbuffer + tkzer.convert_tokens_to_string([tk])
                    curr_incorrect += correctbuffer + tkzer.convert_tokens_to_string([tk])
                    correctbuffer = ""
                    print ("incorrect is now " + incorrect)
                    print ("curr_inc is now " + curr_incorrect)
                    print ("resetting buffer")
                else:
                    incorrect += tkzer.convert_tokens_to_string([tk])
                    curr_incorrect += tkzer.convert_tokens_to_string([tk])
                print ("incorrect is now " + incorrect)
                total += 1
            # extend_encoding(wd, prev, guessct, incorrect, total, compressed)  # bitarray
        #print ("Final dump of correct")
        curr_incorrect, numbers = on_correct(curr_incorrect, numbers)
        #print ("Final dump of incorrect")
        guessct, numbers = on_incorrect(guessct, numbers) # clear buffer after each line

    print("Final encoding")
    total_encoding = numbers + "\n" + incorrect
    print(total_encoding)
    print ("Correct guesses: " + str(compressed))
    print ("Total guesses: " + str(total))
    with open(out_intermfile, 'w') as of:  # This step can be removed in future! Only here now to see outputs and stats
        of.write(total_encoding)
    ie.crunch_bz2(total_encoding, infile + ".comp")
    ogsize = os.path.getsize(infile)
    print ("Size of original file: " + str(ogsize))
    intermsize = os.path.getsize(infile + ".interm")
    print ("Size of intermediate file: " + str(intermsize))
    finalsize = os.path.getsize(infile + ".comp")
    print ("Size of final file: " + str(finalsize))

    ie.crunch_bz2(ftxt, infile + ".bz2")    # crunch for comparison's sake
    bzogsize = os.path.getsize(infile + ".bz2")
    print ("Size of bzipped original file: " + str(bzogsize))
    print ("final encoding is " + total_encoding)

    # writing stuff to stats
    # Model,Test,Window,Top_K,Correct Gs,Total Gs,OG size,Interm size,Final size,Bzip OG size
    with open(statfile, 'a') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow([modelname, infile, window, TOP_K, compressed, total, ogsize, intermsize, finalsize, bzogsize])

    


if __name__ == "__main__":
    pipeline_encode(sys.argv[1:])