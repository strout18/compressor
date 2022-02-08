from transformers import pipeline
import os, sys
import intermediateencoding as ie # make sure it's not confused
import window as utils

# TO DO DECIDE TOP K


def write_window(window, total_encoding):
    total_encoding += window + ","
    return total_encoding

def dump_incorrect(incorrect, total_encoding):
    # dump the buffer of incorrects into encoding
    if len(incorrect) > 0:
        txt = '0,'
        txt += str(len(incorrect)) + ","
        #print ("Length of incorrect is " + str(len(incorrect)))
        # print ("Str with guess and len: " + txt)
        txt += incorrect + ","
        total_encoding += txt
        # print ("Extending from incorrect. Total encoding is now " + total_encoding)
        incorrect = ""
    return incorrect, total_encoding

def dump_correct(guessct, total_encoding):
    if guessct > 0:
        total_encoding += str(guessct) + ","
        # print ("Total encoding now " + total_encoding)
        guessct = 0
    return guessct, total_encoding

def pipeline_encode(argv):
    total_encoding = ""
    incorrect = "" # buffer for storing incorrect guesses continuously
    guessct = 0
    compressed = 0
    total = 0
    infile = argv[0]    # file name
    modelname = argv[1]
    window = argv[2] if len(argv) == 3 else "1"  # window of prev words (0 = from last period?)  
    # should prob error check command line args
    out_intermfile = infile + ".interm"  # file name
    unmasker = pipeline('fill-mask', model=modelname)
    with open(infile, 'r') as inf:
        ftxt = inf.read()
        #print("Writing window")
        total_encoding = write_window(window, total_encoding)
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
            if prev:
            # unmasker = pipeline('fill-mask', model=model, tokenizer=tkzer)
            # guess = unmasker(prev + f"{unmasker.tokenizer.mask_token}")[0]["token_str"]
                guess = unmasker(prev + f"{tkzer.mask_token}")[0]["token_str"]
                print ("The guess is " + guess)
            if prev and guess == tkzer.convert_tokens_to_string([tk]):
                print ("Guess was correct")
                guessct += 1
                compressed += 1
                print ("Guesscount " + str(guessct))
                print ("Dumping incorrect")
                print (incorrect)
                incorrect, total_encoding = dump_incorrect(incorrect, total_encoding)  # clear out incorrect buffer before logging correct
                print ("encoding is now " + total_encoding)
            else:
                print ("Guess was incorrect")
                # print ("Guess count:" + str(guessct))
                print ("Dumping correct")
                guessct, total_encoding = dump_correct(guessct, total_encoding)
                incorrect += tkzer.convert_tokens_to_string([tk])
                print ("incorrect is now " + incorrect)
            total += 1
        #print ("Final dump of correct")
        guessct, total_encoding = dump_correct(guessct, total_encoding)
        #print ("Final dump of incorrect")
        incorrect, total_encoding = dump_incorrect(incorrect, total_encoding) # clear buffer after each line
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