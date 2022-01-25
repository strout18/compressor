import bz2

def crunch_bz2(txt, filepath):
    bytetxt = txt.encode()
    with bz2.open(filepath, "wb") as f:
        f.write(bytetxt)

def uncrunch_bz2(filepath):
    with bz2.open(filepath, "rb") as f:
        content = f.read()
    return content.decode()