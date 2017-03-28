import gensim, logging
import os
class MySentence(object):
    def __init__(self,fname):
        self.fname=fname
    def __iter__(self):
        dirname = os.getcwd()
        for line in open(os.path.join(dirname,self.fname)):
            yield line.split()

def similar_word(word):
    sentences = MySentence('processed_plot_summaries.txt')
    model = gensim.models.Word2Vec(sentences)
    return model.similar_by_word(word)

