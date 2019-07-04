import gensim as gs
import data_manager as dm
import settings as st

documents = [ "Human machine interface for lab abc computer applications",
              "The EPS user interface management system",
              "A survey of user opinion of computer system response time",
              "System and human system engineering testing of EPS",
              "Relation of user perceived response time to error measurement",
              "The generation of random binary unordered trees",
              "The intersection graph of paths in trees",
              "Graph minors IV Widths of trees and well quasi ordering",
              "Graph minors A survey"]

stoplist = set('for a of the and to in'.split())
texts = [[word for word in document. lower() . split() if word not in stoplist] for document in documents]
all_tokens = sum(texts, [])
tokens_once = set(word for word in set(all_tokens) if all_tokens. count(word) == 1)
texts = [[word for word in text if word not in tokens_once] for text in texts]

dictionary = gs.corpora.Dictionary(texts)
dictionary.save('src/tmp/deerwester.dict')

new_doc = "Human computer interaction"
new_vec = dictionary.doc2bow(new_doc. lower() . split())

corpus = [dictionary.doc2bow(text) for text in texts]
# gs.corpora.MmCorpus.serialize('src/tmp/deerwester.mm' , corpus)

# corpus = gs.corpora.MmCorpus('src/tmp/deerwester.mm' )
tfidf = gs.models.TfidfModel(corpus)

corpus_tfidf = tfidf[corpus]

lsi = gs.models.LsiModel(corpus_tfidf, id2word=dictionary, num_topics=2)
corpus_lsi = lsi[corpus_tfidf]
lsi.save('src/tmp/model.lsi' )

lsi.save('src/tmp/model.lsi' )
lsi = gs.models.LsiModel.load('src/tmp/model.lsi' )

doc = "Human computer interaction"
vec_bow = dictionary.doc2bow(doc.lower().split())
vec_lsi = lsi[vec_bow]

index = gs.similarities.MatrixSimilarity(lsi[corpus])
index.save('src/tmp/deerwester.index' )
index = gs.similarities.MatrixSimilarity.load('src/tmp/deerwester.index' )

sims = index[vec_lsi]
sims = sorted(enumerate(sims), key=lambda item: -item[0])
print(sims)

class LawAnalyzer():
    def __init__(self, laws_json):
        self.new_law = dm.get_new_law(laws_json)
        self.old_law = dm.get_old_law(laws_json)

    def save_law(self, law):
        pass

    def load_corpus(self):
        pass

class Corpus():
    def __iter__(self):
        pass