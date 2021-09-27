import sys, bitarray
import ics_api as ics

total_encoding = bitarray.bitarray()
# how to deal with memory problem? will one bit array eat ram? otherwise have to do buffering manually
# also how to set up decoder? how to distinguish between bits
# way to inspect bits of file?

def extend_encoding(wd, prev):
    print ("The current word is " + wd + "and the previous word is " + prev)
    if prev:
        guess = ics.run_model(prev, length=1, top_k=40)
        print ("The guess is" + guess)
    if prev and guess == wd:
        print ("Guess was correct")
        encoded = bitarray.bitarray('1')
    else:
        print ("guess incorrect")
        wdbits = ''.join(format(ord(i), '08b') for i in wd) # convert to bit string
        print ("encoding " + wd + " as " + wdbits)
        encoded = bitarray.bitarray('0'+ wdbits)    # idk how efficient this is
    total_encoding.extend(encoded)
    

def main(argv):
    infile = argv[0]    # file name
    outfile = infile + ".comp"  # file name
    prev = ""
    with open(infile, 'r') as inf:
        for line in inf:
            for wd in line.split():
                extend_encoding(wd, prev)  # bitarray
                prev = wd
    print(total_encoding.to01())
    with open(outfile, 'wb') as of:
        total_encoding.tofile(of)


if __name__ == "__main__":
    main(sys.argv[1:])