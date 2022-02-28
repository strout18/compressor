import sys, filecmp, os, shutil
from gpt2.src.gpt_encoder import gpt_encode
from gpt2.src.gpt_decoder import gpt_decode
from pipeline.encoder import pipeline_encode
from pipeline.decoder import pipeline_decode
from glob import glob

TEST_FOLDERS = [
    "gpt_gen_small_w8_test"
]

progressf = "runprogress.txt"
WINDOW = 8
TOP_K = 50
failf = "failures.txt"
# PIPELINE_MODELS = ["roberta-large", "google/electra-large-generator", "albert-base-v2", "microsoft/mpnet-base"]
PIPELINE_MODELS = ["roberta-large"]
# TODO- TEST IF MPNET SOLO WILL WORK WITH PIPELINE

def run_gpt():
    with open(progressf, 'a') as pf:
        for folder in TEST_FOLDERS:
            pf.write('Running GPT test on ' + folder + "\n")
            pf.flush()
            newfolderstr = "MgptW" + str(WINDOW) + "K" + str(TOP_K)
            newfolder = "tests/" + folder + "/" + newfolderstr
            os.mkdir(newfolder)
            shutil.copy("tests/" + folder + "/" + folder + ".txt", newfolder)
            gpt_encode([newfolder + "/" + folder + ".txt", str(WINDOW), str(TOP_K)])
            gpt_decode([newfolder + "/" + folder + ".txt.comp", str(TOP_K)])
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
                newfolderstr = "M" + model + str(WINDOW) + "K" + str(TOP_K)
                newfolder = "tests/" + folder + "/" + newfolderstr
                os.mkdir(newfolder)
                shutil.copy("tests/" + folder + "/" + folder + ".txt", newfolder)
                pipeline_encode(["tests/" + folder + "/" + folder + ".txt", model, str(WINDOW)])
                pipeline_decode(["tests/" + folder + "/" + folder + ".txt.comp", model])
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
        # pf.write('Running pipeline tests\n')
        # pf.flush()
        # run_pipeline()
        pf.write('All tests complete!')

if __name__ == "__main__":
    main(sys.argv[1:])
