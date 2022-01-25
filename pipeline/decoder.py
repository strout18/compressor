from transformers import pipeline
import sys
import intermediateencoding as ie
import window as utils

total_decoding = "" 
# todo UNIFORMIZE TOP K - IT'S 40 IN GPT BUT 5 DEFAULT HERE

def read_window(txt):
    cutoff = txt.index(',')
    win = txt[0:cutoff]  # review this
    return int(win)

def pipeline_decode(argv):
    global total_decoding
    infile = argv[0]    # file name
    # window = int(argv[1])    # do error checking
    outfile = infile + ".plaintext"  # file name
    modelname = argv[1]
    tkzer = utils.get_tkzer(modelname)
    ftxt = ie.uncrunch_bz2(infile)
    # with open(infile, 'r') as inf:
    #     ftxt = inf.read()
    # print (ftxt)
    window = read_window(ftxt)
    # print ("reading window as " + str(window))
    pointer = len(str(window)) + 1  # trailing comma
    mask_token = tkzer.mask_token
    unmasker = pipeline('fill-mask', model=modelname)
    while pointer < len(ftxt):
        guess_cutoff = ftxt.index(',', pointer)  
        guessc = ftxt[pointer:guess_cutoff]
        guesslen = len(guessc)
        if int(guessc) == 0:
            # print("Guess char was 0")
            pointer += guesslen + 1 # move pointer to beginning of number bits, comma
            len_cutoff = ftxt.index(',', pointer)
            lenchars = ftxt[pointer : len_cutoff]
            # print ("lenchars are " + lenchars)
            txtlen = int(lenchars)    # gives num of chars in current chunk of unguessed text
            # print("txtlen" + str(txtlen))
            pointer += len(lenchars) + 1  # move pointer to beginning of the original unguessed text, with comma
            txtchars = ftxt[pointer:pointer+txtlen]    # chunk of unguessed text
            # print ("txtchars " + txtchars)
            decoded = "".join(txtchars)
            # print("decoded as " + decoded)
            total_decoding += decoded
            # print ("total decoding now " + total_decoding)
            pointer += txtlen + 1 #push pointer to next section, with comma
        else:
            # print ("Guess char was " + guessc)
            for _ in range(int(guessc)):
                decoding_arr = tkzer.tokenize(total_decoding)
                print ("decoding arr " + str(decoding_arr))
                prev = utils.slice_window(window, decoding_arr, len(decoding_arr), tkzer)
                print ("Running with prev " + prev)
                # guess = ics.run_model(prev, length=1, top_k=40)
                guess = unmasker(prev + f"{mask_token}")[0]["token_str"]
                print ("Guess is " + guess)
                total_decoding += guess
                print ("Total decoding now " + total_decoding)
            pointer += guesslen + 1 # push pointer to next section, comma

    print (total_decoding)
    with open(outfile, 'w') as outf:
        outf.write(total_decoding)


if __name__ == "__main__":
    pipeline_decode(sys.argv[1:])