import mainencoderchar
import ics_api as ics
words = "The dog"
with open('gpt_med_w8.txt', 'a') as f:
    for x in range(1, 5000):
        if (x % 50 == 0):
            print (str(x))
        # if (len(words) > 125):
        #     words = words[-124:]    # to cut down runtime (8 wds with spaces probably less than 125 chars)
        split = mainencoderchar.cleansplit(words)
        # print(str(split))
        txtrange = ics.slice_window(8, split, x)
        # print ("Calling with prev " + txtrange)
        newwd = ics.run_model(txtrange, length=1, top_k=40)
        # print ("New wd " + newwd)
        words += newwd
        # print ("words " + words)
        f.write(newwd)
    # print (words)