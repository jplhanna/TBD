from .models import Movie, UserData, Score, Question
from django.contrib.auth.models import User
import numpy as np

class questionHandler:

    def __init__(self, currUser):
        self._movies=self.getMovies(currUser)
    
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
        print scores
        return best_movie
        