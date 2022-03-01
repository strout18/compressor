import sys, os, csv
from gpt2.src import ics_api as ics
import regex as re
from gpt2.src import intermediateencoding as ie

statfile = "altstats.txt"
window = 8
TOP_K = 40
declare_length = True

# TODO trim off final comma?

def on_correct(incorrect, numbers):
    global declare_length
    # dump the buffer of incorrects into encoding
    if declare_length:
        txt = '0,'
        txt += str(len(incorrect)) + ","
        print ("Length of incorrect is " + str(len(incorrect)))
        print ("Str with guess and len: " + txt)
        numbers += txt
        declare_length = False
        # print ("Extending from incorrect. Total encoding is now " + total_encoding)
    return numbers

def on_incorrect(guessct, numbers):
    # how much to pad to?
    global declare_length
    declare_length = True
    if guessct > 0:
        numbers += str(guessct) + ","
        # print ("Total encoding now " + total_encoding)
        guessct = 0
    return guessct, numbers

# splits array according to decided standards - talk about this in thesis?
def cleansplit(txtstr):
    pat = re.compile(r"""'s|'t|'re|'ve|'m|'ll|\n|'d| ?\p{L}+| ?\p{N}+| ?[^\s\p{L}\p{N}]+|\s+(?!\S)|\s+""") # from encoder.py
    return re.findall(pat, txtstr)

# NOTE : test file that ends in new line

# args = infile, window
def gpt_encode(argv):
    # global total_encoding, incorrect, guessct, compressed, total
    #reset globals
    global window, TOP_K
    numbers = ""
    incorrect = ""
    guessct = 0
    compressed = 0
    total = 0

    infile = argv[0]    # file name 
    # should prob error check command line args
    out_intermfile = infile + ".interm"  # file name
    with open(infile, 'r') as inf:
        ftxt = inf.read()
        #print("Writing window")
        #print ("Encoding now " + total_encoding)
        splat = cleansplit(ftxt)
        print(splat)
        for ct, wd in enumerate(splat):  
            prev = ics.slice_window(int(window), splat, ct) #preceding text
            # print("#" * 40)
            print("Calling extend_encoding on wd \"" + wd + "\" with prev \"" + prev)
            # global guessct, incorrect, total, compressed
            # print ("The current word is " + wd + "and the previous word is " + prev)
            if prev:
                guess = ics.run_model(prev, length=1, top_k=int(TOP_K))
                # print ("The guess is " + guess)
            if prev and guess == wd:
                # print ("Guess was correct")
                guessct += 1
                compressed += 1
                # print ("Guesscount " + str(guessct))
                # print ("Dumping incorrect")
                # print (incorrect)
                print("Dumping incorrect, guess was correct")
                numbers = on_correct(incorrect, numbers)  # clear out incorrect buffer before logging correct
                print ("numbers is now " + numbers)
            else:
                print ("Guess was incorrect")
                # print ("Guess count:" + str(guessct))
                print ("Dumping correct")
                guessct, numbers = on_incorrect(guessct, numbers)
                incorrect += wd
                print ("incorrect is now " + incorrect)
                total += 1
            # extend_encoding(wd, prev, guessct, incorrect, total, compressed)  # bitarray
        #print ("Final dump of correct")
        numbers = on_correct(incorrect, numbers)
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
        csvwriter.writerow(["gpt", infile, window, TOP_K, compressed, total, ogsize, intermsize, finalsize, bzogsize])

    


if __name__ == "__main__":
    gpt_encode(sys.argv[1:])
