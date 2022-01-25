import sys, os, csv
import ics_api as ics
import regex as re
import intermediateencoding as ie

total_encoding = ""
incorrect = "" # buffer for storing incorrect guesses continuously
guessct = 0
compressed = 0
total = 0
statfile = "../../allstats.txt"
TOP_K = 40

def write_window(window):
    global total_encoding
    total_encoding += window + ","

def extend_encoding(wd, prev):
    global guessct
    global incorrect
    global total
    global compressed
    # print ("The current word is " + wd + "and the previous word is " + prev)
    if prev:
        guess = ics.run_model(prev, length=1, top_k=TOP_K)
        # print ("The guess is " + guess)
    if prev and guess == wd:
        # print ("Guess was correct")
        guessct += 1
        compressed += 1
        # print ("Guesscount " + str(guessct))
        # print ("Dumping incorrect")
        # print (incorrect)
        dump_incorrect()  # clear out incorrect buffer before logging correct
        # print ("encoding is now " + total_encoding)
    else:
        # print ("Guess was incorrect")
        # print ("Guess count:" + str(guessct))
        # print ("Dumping correct")
        dump_correct()
        incorrect += wd
        # print ("incorrect is now " + incorrect)
    total += 1

def dump_incorrect():
    # dump the buffer of incorrects into encoding
    global incorrect
    global total_encoding
    if len(incorrect) > 0:
        txt = '0,'
        txt += str(len(incorrect)) + ","
        #print ("Length of incorrect is " + str(len(incorrect)))
        # print ("Str with guess and len: " + txt)
        txt += incorrect + ","
        total_encoding += txt
        # print ("Extending from incorrect. Total encoding is now " + total_encoding)
        incorrect = ""

def dump_correct():
    # how much to pad to?
    global guessct
    if guessct > 0:
        global total_encoding
        total_encoding += str(guessct) + ","
        # print ("Total encoding now " + total_encoding)
        guessct = 0

# splits array according to decided standards - talk about this in thesis?
def cleansplit(txtstr):
    pat = re.compile(r"""'s|'t|'re|'ve|'m|'ll|'d| ?\p{L}+| ?\p{N}+| ?[^\s\p{L}\p{N}]+|\s+(?!\S)|\s+""") # from encoder.py
    return re.findall(pat, txtstr)

# NOTE : test file that ends in new line

# args = infile, window
def gpt_encode(argv):
    infile = argv[0]    # file name
    window = argv[1] if len(argv) == 2 else "1"  # window of prev words (0 = from last period?)  
    # should prob error check command line args
    out_intermfile = infile + ".interm"  # file name
    with open(infile, 'r') as inf:
        ftxt = inf.read()
        #print("Writing window")
        write_window(window)
        #print ("Encoding now " + total_encoding)
        splat = cleansplit(ftxt)
        print(splat)
        for ct, wd in enumerate(splat):  
            prev = ics.slice_window(int(window), splat, ct) #preceding text
            # print("#" * 40)
            # print("Calling extend_encoding on wd \"" + wd + "\" with prev \"" + prev)
            extend_encoding(wd, prev)  # bitarray
        #print ("Final dump of correct")
        dump_correct()
        #print ("Final dump of incorrect")
        dump_incorrect() # clear buffer after each line

    # print("Final encoding")
    # print(total_encoding)
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

    # writing stuff to stats
    # Test,Window,Top_K,Correct Gs,Total Gs,OG size,Interm size,Final size,Bzip OG size
    with open(statfile, 'a') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow([infile, window, TOP_K, compressed, total, ogsize, intermsize, finalsize, bzogsize])

    


if __name__ == "__main__":
    gpt_encode(sys.argv[1:])