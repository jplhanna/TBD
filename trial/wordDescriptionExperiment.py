import os
import csv
from word2vec import *
import gensim, logging

# A movie class that's used to record the information of a Movie
class Movie:
    def __init__(self, name, duration, genres, imdb, keywords, content_rating, year, score):
        self.name = name
        self.duration = duration
        self.genres = genres
        self.imdb = imdb
        self.keywords = keywords
        self.content_rating = content_rating
        self.year = year
        self.score = score

    def __str__(self):
        return "MOVIE: \n" + "name: " + self.name + "\nduration: " + self.duration + "\ngenres: " \
        + self.genres + "\nimdb: " + self.imdb + "\nkeywords: "+ self.keywords + "\ncontent rating: " + self.content_rating \
        + "\nscore: " + self.score + "\nyear: " + self.year + "\n"

# Record all the movies better create another class or use other data structures
MovieList = []
# Read from csv and write to MovieList with selected features
di = os.getcwd()
f = di+'/data/movie_metadata.csv'
with open(f, 'rb') as csvfile:
    r = csv.reader(csvfile,delimiter=',')
    for row in r:
        m = Movie(row[11], row[3], row[9], row[17], row[16], row[21], row[23], row[25])
        MovieList.append(m)
for m in MovieList:
    print m

# Ask users for input
target = raw_input("Please use one word to describe the movie you would like to watch today ==> \n")

# Use word2vec to calculate similarity between two words
# Uncomment this chunk of code for the first time, it's training word2vec model and save it so that if you are using it
# next time, you just need to load it. Training process is super slow, we don't want to wait for it every time.
'''
# save the model first so that the speed will become faster
sentences = MySentence('processed_plot_summaries.txt')
model = gensim.models.Word2Vec(sentences)
model.save('/tools/movieModel')
'''
newModel = gensim.models.Word2Vec.load('/tools')
print newModel.similar_by_word("comedy")
print newModel.similarity("happy", "comedy")
maxM = MovieList[0]
maxSim = 0
for M in MovieList:
    simSum = 0
    keyword = M.keywords.split('|')
    for k in keyword:
        if len(k.split(' '))==1 and k!='' and k.lower() in newModel.vocab:
            simSum += newModel.similarity(target,k.lower())
            print target, k, simSum
    if simSum>maxSim:
        maxSim = simSum
        maxM = M
print maxM


