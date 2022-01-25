import sys, bitarray
import ics_api as ics

total_encoding = bitarray.bitarray()
incorrect = bitarray.bitarray() # buffer for storing incorrect guesses continuously

def write_window(window):
    winarr = bitarray.bitarray(format(window, '08b'))
    total_encoding.extend(winarr)

def extend_encoding(wd, prev):
    # print ("The current word is " + wd + "and the previous word is " + prev)
    space = bitarray.bitarray('00100000') # encoding of space
    # will need to be changed if we go to 16 bit len encoding (lencoding B) )
    if prev:
        guess = ics.run_model(prev, length=1, top_k=40)
        guess = guess[1:]   # trim off leading space
        print ("The guess is " + guess)
    if prev and guess == wd:
        print ("Guess was correct")
        print ("Dumping incorrect")
        print (incorrect.to01())
        dump_incorrect()  # clear out incorrect buffer before logging correct
        encoded = bitarray.bitarray('1')
        total_encoding.extend(encoded)
        print ("encoding is now " + total_encoding.to01())
    else:
        print ("Guess was incorrect")
        wdbits = ''.join(format(ord(i), '08b') for i in wd) # convert to bit string 
        # hopefully this is consistently big endian
        print ("Encoding " + wd + " as " + wdbits)
        if len(incorrect) > 0 or len(total_encoding) > 8: 
            incorrect.extend(space) # this needs to be refined for periods and stuff
        incorrect.extend(wdbits)
        print ("incorrect is now " + incorrect.to01())

def dump_incorrect():
    # dump the buffer of incorrects into encoding
    if len(incorrect) > 0:
        arr = bitarray.bitarray('0')
        ### IMPORTANT - WHAT SHOULD BIT LENGTH OF NUMBER BE? 16 BITS SO >256 CHARS?
        arr.extend(format(len(incorrect) // 8, '08b'))   
        print ("Length of incorrect is " + str(len(incorrect)))
        print ("Array with guess and len bits: " + arr.to01())
        arr.extend(incorrect)
        total_encoding.extend(arr) 
        print ("Extending from incorrect. Total encoding is now " + total_encoding.to01())
        incorrect.clear()

# splits array according to decided standards - talk about this in thesis?
def cleansplit(txtstr):
    return txtstr.split()

def main(argv):
    infile = argv[0]    # file name
    window = int(argv[1]) if len(argv) == 2 else 1  # window of prev words (0 = from last period?)  
    # should prob error check command line args
    outfile = infile + ".comp"  # file name
    with open(infile, 'r') as inf:
        ftxt = inf.read()
        print("Writing window")
        write_window(window)
        print ("Encoding now " + total_encoding.to01())
        for ct, wd in enumerate(cleansplit(ftxt)):  
            prev = ics.slice_window(int(window), ftxt.split(), ct) #preceding text
            print("#" * 40)
            print("Calling extend_encoding on wd \"" + wd + "\" with prev \"" + prev)
            extend_encoding(wd, prev)  # bitarray
        print ("Final dump of incorrect")
        dump_incorrect() # clear buffer after each line
    print("Final encoding")
    print(total_encoding.to01())
    with open(outfile, 'wb') as of:
        total_encoding.tofile(of)


if __name__ == "__main__":
    main(sys.argv[1:])