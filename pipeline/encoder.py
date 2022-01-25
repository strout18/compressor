from transformers import pipeline
import os, sys
import intermediateencoding as ie
import window as utils

# TO DO DECIDE TOP K

total_encoding = ""
incorrect = "" # buffer for storing incorrect guesses continuously
guessct = 0
compressed = 0
total = 0

def write_window(window):
    global total_encoding
    total_encoding += window + ","

def extend_encoding(wd, prev, unmasker, mask_token):
    global guessct
    global incorrect
    global total
    global compressed
    # print ("The current word is " + wd + "and the previous word is " + prev)
    if prev:
        # unmasker = pipeline('fill-mask', model=model, tokenizer=tkzer)
        # guess = unmasker(prev + f"{unmasker.tokenizer.mask_token}")[0]["token_str"]
        guess = unmasker(prev + f"{mask_token}")[0]["token_str"]
        print ("The guess is " + guess)
    if prev and guess == wd:
        print ("Guess was correct")
        guessct += 1
        compressed += 1
        print ("Guesscount " + str(guessct))
        print ("Dumping incorrect")
        print (incorrect)
        dump_incorrect()  # clear out incorrect buffer before logging correct
        print ("encoding is now " + total_encoding)
    else:
        print ("Guess was incorrect")
        # print ("Guess count:" + str(guessct))
        print ("Dumping correct")
        dump_correct()
        incorrect += wd
        print ("incorrect is now " + incorrect)
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
    global guessct
    if guessct > 0:
        global total_encoding
        total_encoding += str(guessct) + ","
        # print ("Total encoding now " + total_encoding)
        guessct = 0

def pipeline_encode(argv):
    infile = argv[0]    # file name
    modelname = argv[1]
    window = argv[2] if len(argv) == 3 else "1"  # window of prev words (0 = from last period?)  
    # should prob error check command line args
    out_intermfile = infile + ".interm"  # file name
    unmasker = pipeline('fill-mask', model=modelname)
    with open(infile, 'r') as inf:
        ftxt = inf.read()
        #print("Writing window")
        write_window(window)
        #print ("Encoding now " + total_encoding)
        tkzer = utils.get_tkzer(modelname)
        splat = tkzer.tokenize(ftxt)    # if we can feed in tokenized stream to pipeline then we can speed this up
        print(splat)
        # as opposed to converting back and forth between token and string
        for ct, tk in enumerate(splat):  
            print ("Tk is " + tk)
            print ("Word version is " + tkzer.convert_tokens_to_string([tk]))
            prev = utils.slice_window(int(window), splat, ct, tkzer)
            print ("prev is " + prev)
            extend_encoding(tkzer.convert_tokens_to_string([tk]), prev, unmasker, tkzer.mask_token)  # the model name and tkzer are usually the same
        #print ("Final dump of correct")
        dump_correct()
        #print ("Final dump of incorrect")
        dump_incorrect() # clear buffer after each line
    # print("Final encoding")
    # print(total_encoding)
    # print("Correct guesses/total: " + str(compressed / total))
    print ("Correct guesses: " + str(compressed))
    print ("Total guesses: " + str(total))
    with open(out_intermfile, 'w') as of:  # This step can be removed in future! Only here now to see outputs and stats
        of.write(total_encoding)
    ie.crunch_bz2(total_encoding, infile + ".comp")
    # orig_ratio = os.path.getsize(infile + ".comp") / os.path.getsize(infile) 
    print ("Size of original file: " + str(os.path.getsize(infile)))
    # print ("Filesize of bz2/original: " + str(orig_ratio))
    print ("Size of intermediate file: " + str(os.path.getsize(infile + ".interm")))
    print ("Size of final file: " + str(os.path.getsize(infile + ".comp")))
    # interm_ratio = os.path.getsize(infile + ".comp") / os.path.getsize(infile + ".interm")
    # print ("Filesize of bz2/pre-bz2 intermediate: " + str(interm_ratio))
    ie.crunch_bz2(ftxt, infile + ".bz2")
    print ("Size of bzipped original file: " + str(os.path.getsize(infile + ".bz2")))

    


if __name__ == "__main__":
    pipeline_encode(sys.argv[1:])