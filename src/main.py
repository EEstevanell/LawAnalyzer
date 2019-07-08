import gensim as gs
import data_manager as dm
import settings as st

class LawAnalyzer():
    def __init__(self, laws_json):
        self.new_law = dm.get_new_law(laws_json)
        self.old_law = dm.get_old_law(laws_json)
        self.stoplist = set('for a of the and to in'.split())

    def save_law(self, law):
        l_id = law['id']
        directory = st.get_law_directory(l_id)

        #if law already was saved then don't append in index table
        laws = self.get_all_laws()
        if not str(l_id) in laws:
            #save law id in the laws index table
            with open(f"{st.law_index_file}",'a') as index_file:
                print(l_id, file = index_file)

        with open(st.get_law_index_file(l_id), 'w') as index_file:
            for key in law.keys():
                if key != "id":
                    #save article address in the law's index table
                    print(key, file = index_file)

                    #save article info
                    article = law[key]
                    with open(f"{directory}/{key}","w") as fd:
                        # TODO use a tokenizer that removes punctuation marks
                        texts = [[word for word in document.lower().split() if word not in self.stoplist] for document in article]
                        for paragraph in texts:
                            for word in paragraph:
                                print(word, file = fd, end = ",")
                            print(file = fd)

    def load_corpus(self):
        laws = self.get_all_laws()
        docs = []
        for l_id in laws:
            directory = st.get_law_directory(l_id)
            for article in self.get_articles(l_id):
                with open(f"{directory}/{article}") as article_fd:
                    docs += [line.split(',')[:-1] for line in article_fd.readlines()]

        dictionary = gs.corpora.Dictionary(docs)
        return dictionary, docs

    def get_articles(self, law_id):
        index = open(st.get_law_index_file(law_id))
        arts_id = []
        art_id = index.readline()
        while art_id:
            arts_id.append(art_id[:-1])
            art_id = index.readline()

        index.close()
        return arts_id

    def get_paragraphs(self, article):
        l_id = self.new_law['id']
        directory = st.get_law_directory(l_id)
        paragraphs = []
        with open(f'{directory}/{article}') as fd:
            paragraphs += [line.split(',')[:-1] for line in fd.readlines()]
        
        return paragraphs


    def get_all_laws(self):
        index = open(st.law_index_file)
        laws_id = []
        law_id = index.readline()
        while law_id:
            laws_id.append(law_id[:-1])
            law_id = index.readline()

        index.close()
        return laws_id

    def transform_to_lsi(self):
        d, texts = self.load_corpus()
        corpus = [d.doc2bow(text, allow_update=True) for text in texts]
        # TODO: See number of topics
        lsi = gs.models.LsiModel(corpus, id2word=d, num_topics=2) # initialize an LSI transformation
        # lsi.save(f'{st.law_lsi_file}')
        return lsi, corpus, d


    def get_similarities(self, article):
        paragraphs = self.get_paragraphs(article)
        sims = []

        lsi, corpus, dic = self.transform_to_lsi()
        
        for p in paragraphs:
            vec_bow = dic.doc2bow(p)
            vec_lsi = lsi[vec_bow]
            index = gs.similarities.MatrixSimilarity(lsi[corpus])  # transform corpus to LSI space and index it
            sims.append(list(enumerate(index[vec_lsi]))) 

        return sims # perform a similarity query against the corpus


    def query(self, article):
        sims = self.get_similarities(article)



if __name__ == '__main__':
    la = LawAnalyzer(r"src/test/testing_law_1.json")
    la.save_law(la.new_law)
    la.save_law(la.old_law)
    d = la.load_corpus()
    la.transform_to_lsi()
    similarities = la.get_similarities('1')
    print(similarities)