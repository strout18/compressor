import gpt2.src.gpt_encoder as enc
import gpt2.src.ics_api as ics
from itertools import cycle
# words = "The dog"
seeds = ["The dog", "The carpenter saw the fog", "So the walrus said", "On a balcony", 
    "Waterfalls never", "But how can that be possible", "The cat", "You would do it too",
    "Elect me president and", "Should you even be aware", "The economy rose by twelve",
    "Cry me a river because", "whatever because he's in love!", "The lamp sat creatively",
    "Can you tell I'm bored", "This thesis is taking my serotonin", "Over eleven thousand",
    "Prepare to die", "I am your father", "You're gonna need a bigger", "My wife in a funny voice"
]
# seedpool = cycle(seeds)
# words = ""
for ct, seed in enumerate(seeds):
    with open('gpt_med_w8_seed' + str(ct) + ".txt", 'a+') as f:
        words = seed
        f.write(seed)
        for x in range(1, 500):
            if (x % 50 == 0):
                print (str(x))
            # if (len(words) > 125):
            #     words = words[-124:]    # to cut down runtime (8 wds with spaces probably less than 125 chars)
            split = enc.cleansplit(words)
            # print(str(split))
            txtrange = ics.slice_window(8, split, x)
            # print ("Calling with prev " + txtrange)
            newwd = ics.run_model(txtrange, length=1, top_k=40)
            # print ("New wd " + newwd)
            words += newwd
            # print ("words " + words)
            f.write(newwd)
# with open('gpt_med_w8_v4.txt', 'a') as f:
#     for seed in seeds:
#         words = seed
#         f.write(words)
#         for x in range (1, 238):
#             if (x % 50 == 0):
#                 print(str(x))
#             split = enc.cleansplit(words)
#             txtrange = ics.slice_window(8, split, x)
#             newwd = ics.run_model(txtrange, length=1, top_k=40)
#             words += newwd
#             f.write(newwd)


    # for y in range(0, 15):
    #     newseed = next(seedpool)
    #     words += newseed
    #     f.write(newseed)
    #     for x in range(1, 350):     # guessing this is a good number to stop the train from going off the rails
    #         if (x % 50 == 0):
    #             print (str(x))
    #         split = enc.cleansplit(words)
    #         # print(str(split))
    #         txtrange = ics.slice_window(8, split, x)
    #         # print ("Calling with prev " + txtrange)
    #         newwd = ics.run_model(txtrange, length=1, top_k=40)
    #         # print ("New wd " + newwd)
    #         words += newwd
    #         # print ("words " + words)
    #         f.write(newwd)
    
        
    # for x in range(1, 5000):
    #     if (x % 50 == 0):
    #         print (str(x))
    #     # if (len(words) > 125):
    #     #     words = words[-124:]    # to cut down runtime (8 wds with spaces probably less than 125 chars)
    #     split = gpt_encoder.cleansplit(words)
    #     # print(str(split))
    #     txtrange = ics.slice_window(8, split, x)
    #     # print ("Calling with prev " + txtrange)
    #     newwd = ics.run_model(txtrange, length=1, top_k=40)
    #     # print ("New wd " + newwd)
    #     words += newwd
    #     # print ("words " + words)
    #     f.write(newwd)
    # # print (words)
