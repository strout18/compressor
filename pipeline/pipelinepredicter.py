import window as utils
from transformers import pipeline
words = "The dog was very big so" # TODO INITIALIZE FILE WITH THESE WORDS
modelname = "roberta-large"
tkzer = utils.get_tkzer(modelname)
unmasker = pipeline('fill-mask', model=modelname)
with open('roberta-large_med_w8.txt', 'a') as f:
    for x in range(6, 5006):
        if (x % 50 == 0):
            print (str(x))
        # if (len(words) > 125):
        #     words = words[-124:]    # to cut down runtime (8 wds with spaces probably less than 125 chars)
        split = tkzer.tokenize(words)
        print ("tokens are " + str(split))
        # print(str(split))
        txtrange = utils.slice_window(8, split, x, tkzer)
        # txtrange = ics.slice_window(8, split, x)
        print ("Calling with prev " + txtrange)
        guess = unmasker(txtrange + f"{tkzer.mask_token}")[0]["token_str"]
        print ("guess " + guess)
        # print (str(guess.isalpha()))
        # if not guess.isalpha() and guess != ".":
        #     guess = "The"
        #     print ("here")
        words += guess
        # print ("words " + words)
        f.write(guess)
    # print (words)
