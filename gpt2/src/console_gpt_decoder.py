import sys
import ics_api as ics
import regex as re
import intermediateencoding as ie
 

def read_window(txt):
    cutoff = txt.index(',')
    win = txt[0:cutoff]  # review this
    return int(win)

def gpt_decode(argv):
    total_decoding = ""
    infile = argv[0]    # file name
    # window = int(argv[1])    # do error checking
    outfile = infile + ".plaintext"  # file name
    ftxt = ie.uncrunch_bz2(infile)
    # with open(infile, 'r') as inf:
    #     ftxt = inf.read()
    # print (ftxt)
    window = read_window(ftxt)
    # print ("reading window as " + str(window))
    pointer = len(str(window)) + 1  # trailing comma
    while pointer < len(ftxt):
        guess_cutoff = ftxt.index(',', pointer)  
        guessc = ftxt[pointer:guess_cutoff]
        guesslen = len(guessc)
        if int(guessc) == 0:
            print("Guess char was 0")
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
            print("decoded as " + decoded)
            total_decoding += decoded
            # print ("total decoding now " + total_decoding)
            pointer += txtlen + 1 #push pointer to next section, with comma
        else:
            print ("Guess char was " + guessc)
            pat = re.compile(r"""'s|'t|'re|'ve|'m|'ll|'d| ?\p{L}+| ?\p{N}+| ?[^\s\p{L}\p{N}]+|\s+(?!\S)|\s+""") # from encoder.py
            for _ in range(int(guessc)):
                decoding_arr = re.findall(pat, total_decoding)
                # print ("decoding arr " + str(decoding_arr))
                prev = ics.slice_window(window, decoding_arr, len(decoding_arr))
                print ("Running with prev " + prev)
                guess = ics.run_model(prev, length=1, top_k=40)
                print ("Guess is " + guess)
                total_decoding += guess
                print ("Total decoding now " + total_decoding)
            pointer += guesslen + 1 # push pointer to next section, comma

    print (total_decoding)
    with open(outfile, 'w') as outf:
        outf.write(total_decoding)


if __name__ == "__main__":
    gpt_decode(sys.argv[1:])