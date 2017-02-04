import gensim, logging
import os
def preprocess(filename):
    path=os.getcwd() + '/MovieSummaries/'
    f=open(os.path.join(path,filename))
    target = open(os.getcwd()+'/processed_plot_summaries.txt','w')
    for line in f:
        target.write(line[9:])
    target.close()
    f.close()
class MySentence(object):
    def __init__(self,fname):
        self.fname=fname
    def __iter__(self):
        dirname = os.getcwd()
        for line in open(os.path.join(dirname,self.fname)):
            yield line.split()
sentences = MySentence('processed_plot_summaries.txt')
model = gensim.models.Word2Vec(sentences)

print model.similar_by_word('anti-utopia')
