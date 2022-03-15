import arcode
import bz2

def transform(intermfile):
    with open(intermfile, 'r') as inf:
        ftxt = inf.read()
        nums, incorrect = ftxt.split('\n', 1)
        with open(intermfile+'.num', 'w') as outf:
            outf.write(nums)
        with open(intermfile+'.inc', 'w') as outf:
            outf.write(incorrect)
        ar = arcode.ArithmeticCode(use_static_model)
        ar.encode_file(intermfile+'.num', intermfile+'.ae')
        with bz2.open(intermfile+'.wds', "wb") as f:
            bytetext = incorrect.encode()
            f.write(bytetext)
