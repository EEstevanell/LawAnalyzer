import os

corpus_directory = "src/corpora/"

def get_law_directory(law_id):
    try:
        os.makedirs(f"{corpus_directory}/{law_id}")
    except:
        pass
    return f"{corpus_directory}/{law_id}"