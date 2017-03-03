import gensim, logging
import os
class MySentence(object):
    def __init__(self,fname):
        self.fname=fname
    def __iter__(self):
        dirname = os.getcwd()
        for line in open(os.path.join(dirname,self.fname)):
            yield line.split()
