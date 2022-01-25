import sys, bitarray
import ics_api as ics

total_decoding = "" 
# prob should encode window size into file

def read_window(bits):
    win = bits[0:8].to01()
    return int(win, 2)

def main(argv, total_decoding):
    infile = argv[0]    # file name
    # window = int(argv[1])    # do error checking
    outfile = infile + ".plaintext"  # file name
    bits = bitarray.bitarray()  # will reading it all into memory at once be a problem?
    with open(infile, 'rb') as inf:
        bits.fromfile(inf)
    print (bits.to01())
    window = read_window(bits)
    print ("reading window as " + str(window))
    pointer = 8
    while pointer < len(bits) - 8:  ## minus 8 lets us cut off padding 
        guessbit = bits[pointer]
        if guessbit == False:
            print("Guess bit was false")
            pointer += 1 # move pointer to beginning of number bits
            lenbits = bits[pointer:pointer + 8].to01()
            print ("lenbits are " + lenbits)
            txtlen = int(lenbits, 2)    # gives num of chars in current chunk of unguessed text
            print("txtlen" + str(txtlen))
            pointer += 8   # move pointer to beginning of the original unguessed text
            # NOTE: IF LENGTH OF NUMBER > 256 THIS NEEDS TO BE RECONFIGURED
            txtbits = bits[pointer:pointer+8*txtlen]    # chunk of unguessed text
            print ("txtbits " + txtbits.to01())
            splitbits = [txtbits[i:i+8].to01() for i in range(0, len(txtbits), 8)] # unguessed text split
            print ("splitbits " + str(splitbits))
            decoded = "".join([chr(int(bitstring, 2)) for bitstring in splitbits])  # TO DO: DEAL WITH SPACES
            print("decoded as " + decoded + ".")
            total_decoding += decoded
            print ("total decoding now " + total_decoding)
            pointer += 8 * txtlen #push pointer to next section
        else:
            print ("Guess bit was correct")
            decoding_arr = total_decoding.split()
            prev = ics.slice_window(window, decoding_arr, len(decoding_arr))
            print ("Running with prev " + prev)
            guess = ics.run_model(prev, length=1, top_k=40)
            print ("Guess is " + guess)
            total_decoding += guess
            print ("Total decoding now " + total_decoding)
            pointer += 1 # push pointer to next section

    print (total_decoding)
    with open(outfile, 'w') as outf:
        outf.write(total_decoding)


if __name__ == "__main__":
    main(sys.argv[1:], total_decoding)