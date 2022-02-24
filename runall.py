import sys, filecmp, os
from gpt2.src.gpt_encoder import gpt_encode
from gpt2.src.gpt_decoder import gpt_decode
from pipeline.encoder import pipeline_encode
from pipeline.decoder import pipeline_decode
from glob import glob

TEST_FOLDERS = [
    "dde_unspeech", "gpt_gen_small_w8", "random_small", "random_med", "falklands_wiki", "mlk_vietnam",
    "sherlock_bpp", "frederick_wiki", "obama_inaug", "simple_custom", "gatsby_intro", 
    "orwell_af", "woolf_essays"
]

progressf = "runprogress.txt"
WINDOW = 5
failf = "failures.txt"
# PIPELINE_MODELS = ["roberta-large", "google/electra-large-generator", "albert-base-v2", "microsoft/mpnet-base"]
PIPELINE_MODELS = ["roberta-large"]
# TODO- TEST IF MPNET SOLO WILL WORK WITH PIPELINE

def run_gpt():
    with open(progressf, 'a') as pf:
        for folder in TEST_FOLDERS:
            pf.write('Running GPT test on ' + folder + "\n")
            pf.flush()
            gpt_encode(["tests/" + folder + "/" + folder + ".txt", str(WINDOW)])
            gpt_decode(["tests/" + folder + "/" + folder + ".txt.comp"])
            comparison = filecmp.cmp(
                "tests" + "/" + folder + "/" + folder + ".txt", "tests" + "/" + folder + "/" + folder + ".txt.comp.plaintext", shallow=False
            )
            if not comparison:
                with open(failf, 'a') as ff:
                    ff.write("Failure with model gpt on folder "  + folder +  "with a top_k of ? and a window of " + str(WINDOW))
                pf.write("Diff test failed on " + folder + "\n")
                pf.flush()
        pf.write("GPT tests complete!\n")
        pf.flush()

def clear_files():
    for f in glob('./tests/*/*.txt.*'):
        os.remove(f)

def basic_test_gpt():
    with open(progressf, 'a') as pf:
        folder = "simple_custom"
        pf.write('Running GPT test on ' + folder + "\n")
        print('Running GPT test on ' + folder + "\n")
        pf.flush()
        gpt_encode(["tests/" + folder + "/" + folder + ".txt", str(WINDOW)])
        gpt_decode(["tests/" + folder + "/" + folder + ".txt.comp"])
        comparison = filecmp.cmp(
                "tests/" + folder + "/" + folder + ".txt", "tests/" + folder + "/" + folder + ".txt.comp.plaintext", shallow=False
            )
        if not comparison:
            with open(failf, 'a') as ff:
                ff.write("Failure with model gpt on folder "  + folder +  "with a top_k of ? and a window of " + str(WINDOW))
            pf.write("Diff test failed on " + folder + "\n")
            pf.flush()
        pf.write("GPT tests complete!\n")
        pf.flush()

def run_pipeline():
    with open(progressf, 'a') as pf:
        for model in PIPELINE_MODELS:
            pf.write('Testing ' + model + ' model\n')
            for folder in TEST_FOLDERS:
                pf.write('Running ' + model + ' test on ' + folder + "\n")
                pf.flush()
                pipeline_encode(["tests/" + folder + "/" + folder + ".txt", model, str(WINDOW)])
                pipeline_decode(["tests/" + folder + "/" + folder + ".txt.comp", model])
                comparison = filecmp.cmp(
                "tests/" + folder + "/" + folder + ".txt", "tests/" + folder + "/" + folder + ".txt.comp.plaintext", shallow=False
                )
                if not comparison:
                    with open(failf, 'a') as ff:
                        ff.write("Failure with model " + model + " on folder "  + folder +  "with a top_k of ? and a window of " + str(WINDOW))
                    pf.write("Diff test failed on " + folder + "\n")
                    pf.flush()
        pf.write("Pipeline tests complete!\n")


def main(argv):
    with open(progressf, 'a') as pf:
        clear_files()
        pf.write('Running GPT tests\n')
        pf.flush()
        # basic_test_gpt()
        run_gpt()
        pf.write('Clearing files...\n')
        pf.flush()
        clear_files()
        pf.write('Running pipeline tests\n')
        pf.flush()
        run_pipeline()
        # pf.write('Clearing files...')
       # clear_files()
        pf.write('All tests complete!')

if __name__ == "__main__":
    main(sys.argv[1:])
