from transformers import RobertaTokenizer, ElectraTokenizer, AlbertTokenizer, MPNetTokenizer, BertTokenizer

def get_tkzer(modelname):
    if modelname[:7] == "roberta": # todo add other models
        return RobertaTokenizer.from_pretrained(modelname)
    if modelname[:14] == "google/electra":
        return ElectraTokenizer.from_pretrained(modelname)
    if modelname[:6] == "albert":
        return AlbertTokenizer.from_pretrained(modelname)
    if modelname[:15] == "microsoft/mpnet":
        return MPNetTokenizer.from_pretrained(modelname)
        # shitty tokenizers
    if modelname[:4] == "bert":
        return BertTokenizer.from_pretrained(modelname)
    return MPNetTokenizer.from_pretrained(modelname)
    # shitty tokenizers


def slice_window(winlen, tkarr, index, tkzer):
    # todo deal with when winlen = 0
    # if index == 0:
    #     return txtarr[0]
    if index < winlen:  # slice from start of line til word if line (up til word) is shorter than window
        return tkzer.convert_tokens_to_string(tkarr[:index])
    else:
        start = index - winlen
        return tkzer.convert_tokens_to_string(tkarr[start:index])
