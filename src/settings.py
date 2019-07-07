import os

corpus_directory = "src/corpora/"
law_index_file = f"{corpus_directory}/index.law"

def get_law_index_file(law_id):
    return f"{get_law_directory(law_id)}/index.arts"

def get_law_directory(law_id):
    try:
        os.makedirs(f"{corpus_directory}/{law_id}")
        return f"{corpus_directory}/{law_id}"
    except:
        pass
    return f"{corpus_directory}/{law_id}"