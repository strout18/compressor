import sys, filecmp, os, shutil
from alt_gpt_encoder import gpt_encode
from alt_gpt_decoder import gpt_decode
from pipeline.altencoder import pipeline_encode
from pipeline.altdecoder import pipeline_decode

TEST_FOLDERS = [
    "dde_unspeech", "gpt_gen_small_w8", "random_small", "random_med", "falklands_wiki", "mlk_vietnam",
    "sherlock_bpp", "frederick_wiki", "obama_inaug", "simple_custom", "gatsby_intro", 
    "orwell_af", "woolf_essays", "gpt_med_w8_v5"
]

WINDOW = 10
TOP_K = 40
progressf = "ALT/failures/altrunprogressW" + str(WINDOW) + "K" + str(TOP_K) + ".txt"
failf = "altfailures.txt"
# PIPELINE_MODELS = ["roberta-large", "google/electra-large-generator", "albert-base-v2", "microsoft/mpnet-base"]
PIPELINE_MODELS = ["roberta-large"]
# PIPELINE_MODELS = []
# TODO- TEST IF MPNET SOLO WILL WORK WITH PIPELINE

def run_gpt():
    with open(progressf, 'a+') as pf:
        for folder in TEST_FOLDERS:
            pf.write('Running GPT test on ' + folder + "\n")
            pf.flush()
            newfolderstr = "ALT_MgptW" + str(WINDOW) + "K" + str(TOP_K)
            newfolder = "tests/" + folder + "/" + newfolderstr
            os.mkdir(newfolder)
            shutil.copy("tests/" + folder + "/" + folder + ".txt", newfolder)
            gpt_encode([newfolder + "/" + folder + ".txt", WINDOW, TOP_K])
            gpt_decode([newfolder + "/" + folder + ".txt.comp", WINDOW, TOP_K])
            comparison = filecmp.cmp(
                newfolder + "/" + folder + ".txt", newfolder + "/" + folder + ".txt.comp.plaintext", shallow=False
            )
            if not comparison:
                with open(failf, 'a') as ff:
                    ff.write("Failure with model gpt on folder "  + folder +  "with a top_k of " + str(TOP_K) + " and a window of " + str(WINDOW))
                pf.write("Diff test failed on " + folder + "\n")
                pf.flush()
        pf.write("GPT tests complete!\n")
        pf.flush()

# def clear_files():
#     for f in glob('./tests/*/*.txt.*'):
#         os.remove(f)

def basic_test_gpt():
    with open(progressf, 'a') as pf:
        folder = "simple_custom"
        pf.write('Running GPT test on ' + folder + "\n")
        print('Running GPT test on ' + folder + "\n")
        pf.flush()
        newfolderstr = "MgptW" + str(WINDOW) + "K" + str(TOP_K)
        newfolder = "tests/" + folder + "/" + newfolderstr
        os.mkdir(newfolder)
        shutil.copy("tests/" + folder + "/" + folder + ".txt", newfolder)
        gpt_encode([newfolder + "/" + folder + ".txt", str(WINDOW), str(TOP_K)])
        gpt_decode([newfolder + "/" + folder + ".txt.comp", str(TOP_K)])
        comparison = filecmp.cmp(newfolder + "/" + folder + ".txt", newfolder + "/" + folder + ".txt.comp.plaintext", shallow=False)
        if not comparison:
            with open(failf, 'a') as ff:
                ff.write("Failure with model gpt on folder "  + folder +  "with a top_k of " + str(TOP_K) + " and a window of " + str(WINDOW))
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
                newfolderstr = "ALT_M" + model + str(WINDOW) + "K" + str(TOP_K)
                newfolder = "tests/" + folder + "/" + newfolderstr
                os.mkdir(newfolder)
                shutil.copy("tests/" + folder + "/" + folder + ".txt", newfolder)
                pipeline_encode([newfolder + "/" + folder + ".txt", model, str(WINDOW)])
                pipeline_decode([newfolder + "/" + folder + ".txt.comp", model, str(WINDOW)])
                comparison = filecmp.cmp(newfolder + "/" + folder + ".txt", newfolder + "/" + folder + ".txt.comp.plaintext", shallow=False)
                if not comparison:
                    with open(failf, 'a') as ff:
                        ff.write("Failure with model " + model + " on folder "  + folder +  "with a top_k of ? and a window of " + str(WINDOW))
                    pf.write("Diff test failed on " + folder + "\n")
                    pf.flush()
        pf.write("Pipeline tests complete!\n")


def main(argv):
    with open(progressf, 'a') as pf:
        pf.write('Running GPT tests\n')
        pf.flush()
        # basic_test_gpt()
        run_gpt()
        pf.write('Running pipeline tests\n')
        pf.flush()
        run_pipeline()
        pf.write('All tests complete!')

if __name__ == "__main__":
    main(sys.argv[1:])
