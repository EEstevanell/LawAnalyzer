import gensim as gs
import data_manager as dm
import settings as st
import sys

class LawAnalyzer():
    def __init__(self):
        self._pindex_to_articles = []
        self._pindex_to_law = []
        self._pindex_to_paragraph = []

    def build(self, laws_json):
        self.stoplist = set('for a of the and to in'.split())
        self.new_law = dm.get_new_law(laws_json)
        self.old_law = dm.get_old_law(laws_json)

    def _save_pinfo(self, line, law_id, article_id, pindex):
        self._pindex_to_articles.append(article_id)
        self._pindex_to_law.append(law_id)
        self._pindex_to_paragraph.append(pindex[0])
        pindex[0] += 1
        return line.split(',')[:-1]

    def get_law_by_index(self, index):
        return self._pindex_to_law[index]

    def get_article_by_index(self, index):
        return self._pindex_to_articles[index]

    def get_paragraph_by_index(self, index):
        return self._pindex_to_paragraph[index]

    def save_law(self, law):
        l_id = law['id']
        directory = st.get_law_directory(l_id)

        # if law already was saved then don't append in index table
        laws = self.get_all_laws()
        if not str(l_id) in laws:
            # save law id in the laws index table
            with open(f"{st.law_index_file}", 'a') as index_file:
                print(l_id, file=index_file)

        with open(st.get_law_index_file(l_id), 'w') as index_file:
            for key in law.keys():
                if key != "id":
                    # save article address in the law's index table
                    print(key, file=index_file)

                    # save article info
                    article = law[key]
                    with open(f"{directory}/{key}", "w") as fd:
                        # TODO use a tokenizer that removes punctuation marks
                        texts = [[word for word in document.lower().split(
                        ) if word not in self.stoplist] for document in article]
                        for paragraph in texts:
                            for word in paragraph:
                                print(word, file=fd, end=",")
                            print(file=fd)

    def load_corpus(self):
        ignore_law_id = self.new_law["id"]
        laws = self.get_all_laws()
        docs = []
        for l_id in laws:
            if l_id != str(ignore_law_id):
                directory = st.get_law_directory(l_id)
                for article in self.get_articles(l_id):
                    with open(f"{directory}/{article}") as article_fd:
                        i = [0]
                        docs += [self._save_pinfo(line, l_id, article, i)
                                 for line in article_fd.readlines()]

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

    def save_model(self):
        d, texts = self.load_corpus()
        corpus = [d.doc2bow(text, allow_update=True) for text in texts]
        # TODO: See number of topics
        # initialize an LSI transformation
        lsi = gs.models.LsiModel(corpus, id2word=d, num_topics=200)
        lsi.save(st.model_lsi)
        gs.corpora.MmCorpus.serialize(st.model_corpus, corpus)
        d.save(st.model_dic)

    def get_similarities(self, article):
        paragraphs = self.get_paragraphs(article)
        sims = []

        lsi = gs.models.LsiModel.load(st.model_lsi)
        dic = gs.corpora.Dictionary.load(st.model_dic)
        corpus = gs.corpora.MmCorpus(st.model_corpus)

        # transform corpus to LSI space and index it
        index = gs.similarities.MatrixSimilarity(lsi[corpus], num_features=len(dic))

        for p in paragraphs:
            vec_bow = dic.doc2bow(p)
            vec_lsi = lsi[vec_bow]
            # perform a similarity query against the corpus
            sims.append(list(enumerate(index[vec_lsi])))

        return sims  

    def query(self, article):
        sims = self.get_similarities(article)
        return self._get_all_rel(sims)

    def get_best_rel(self, sims):
        if not sims:
            raise Exception("Corpus must be loaded first")

        results = []
        old_law_id = str(self.old_law["id"])

        for docs in sims:
            # index = max(docs, key = lambda x: x[-1])[0]
            for sim in docs:
                if self.get_law_by_index(sim[0]) == old_law_id:
                    results.append((self.get_law_by_index(sim[0]),
                                    self.get_article_by_index(sim[0]),
                                    self.get_paragraph_by_index(sim[0]),
                                    sim[1]))
        return results
        
    def _get_all_rel(self, sims):
        if not sims:
            raise Exception("Corpus must be loaded first")

        results = []
        old_law_id = str(self.old_law["id"])

        for docs in sims:
            sim = max(
                docs, key=lambda x: x[-1] if self.get_law_by_index(x[0]) == old_law_id else -0.9e18)
            results.append((self.get_law_by_index(sim[0]),
                            self.get_article_by_index(sim[0]),
                            self.get_paragraph_by_index(sim[0]),
                            sim[1]))
        return results


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("usage: python main.py <laws-json> <article>")
        exit()

    la = LawAnalyzer()
    la.build(sys.argv[1])
    la.save_law(la.new_law)
    la.save_law(la.old_law)
    d = la.load_corpus()
    la.save_model()
    similarities = la.get_similarities(sys.argv[2])
    print(similarities)
    print(f"results: {la._get_all_rel(similarities)}")
    print(f"results (only best): {la.get_best_rel(similarities)}")
