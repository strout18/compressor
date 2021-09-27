import sys, bitarray

def get_decoding(wd):
    # returns tuple? (whether symbol is ready to be written, value of symbol if ready)
    pass

def main(argv):
    infile = argv[0]    # file name
    outfile = infile + ".plaintext"  # file name
    bits = bitarray.bitarray()  # will reading it all into memory at once be a problem?
    with open(infile, 'r') as inf:
        bits.fromfile(inf)
    print (bits.to01())
    # with open(outfile, 'w') as outf:
    #     for bit in bits:
    #         (done, val) = get_decoding(bit)
    #         if done:
    #             outf.write(val)


if __name__ == "__main__":
    main(sys.argv[1:])