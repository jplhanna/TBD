from .models import Movie, UserData, Score, Question
from django.contrib.auth.models import User
import numpy as np

'''
questionHandler: A simple static class used by the question system in views.py

Representation invariant: self._movies: should always equal a list of movie objects from the sqlite database. The list should only contain movies which are streamed by a 
                          service that the user declares they have. Otherwise all movies

Abstraction function: self.movies=[movie_A, movie_B,...] where movies_A is in movies and for every true in the current users UserData, at least 1 must be true in movies_A
'''
class questionHandler:
    '''
    __init__: initializes the questionHandler based on the user
    modifies: sets self._movies to the correct listings based on rep invariant
    '''
    def __init__(self, currUser):
        self._movies=self.getMovies(currUser)
    
    '''
    getMovies: helps intialize self.movies based on the current user
    input: currUser: A django user object
    output: a list of movie objects
    '''
    def getMovies(self, currUser):
        movies=Movie.objects.all()
        if(currUser.username==""):
            return movies
        userData=UserData.objects.filter(user=currUser)[0]
        if userData.showAll==True:
            return movies
        if userData.netflix == True:
            movies = movies.filter(netflix=True)
        if userData.amazon == True:
            movies = movies.filter(amazon=True)
        if userData.amazonPrime == True:
            movies = movies.filter(amazonPrime=True)
        if userData.hulu == True:
            movies = movies.filter(hulu=True)
        if userData.googlePlay == True:
            movies. movies.filter(googlePlay=True)
        return movies

    '''
    getBestMovie: A method used by the handleQuestions method within views.py when the user finishes the questionaire, in order to return a movie
    input: QA: A list of integers which corresponds to the responses made by the user
           questions: A list of question objects which the were presented to the user
    output: A movie object
    '''
    def getBestMovie(self, QA, questions):
        movies = self._movies
        scores = [float(0)] * len(movies)
        idToLocation = {}
        for _movie_itr_tmp in range(0, len(movies)):
            idToLocation[movies[_movie_itr_tmp].id] = _movie_itr_tmp
        for itr in range(0, len(QA)):
            if int(QA[itr]) == 0:
                break
            choices = Score.objects.filter(question_id=int(questions[itr])).all()
            for choice in choices:
                if choice.movie_id in idToLocation:
                    scores[idToLocation[choice.movie_id]] += float(QA[itr]) * float(choice.score) * movies[idToLocation[choice.movie_id]].popularity
        scores = np.matrix(scores)
        best_movie = movies[np.argmax(scores)]
        return best_movie
        