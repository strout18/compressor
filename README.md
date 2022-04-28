# compressor
Written by Stella Trout in fulfilment of a Reed College thesis.

The main portion of the code that powers the compressor for the GPT-2 model is in `/gpt2/src/gpt_encoder.py` and `/gpt2/src/gpt_decoder.py` .

The equivalent for RoBERTa (and applicable to all models available from Hugginface) is in `pipeline/encoder.py` and `pipeline.decoder.py`. 

The `tests` directory contains the test files used on our compressor. 

Code used to run the tests include files like `runall.py` and `altrunall.py`, which differ in the compressor's level of optimization. 
