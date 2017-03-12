from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Movie(models.Model):
    
    #gotta figure out review configuration
    
    '''
    create:initializer method. sets values for current movie object
    input: title: string containing the title of a movie
           imdb: a string which is the imdb to a movie
           duration: an integer for the number of minutes the movie goes
           year: an integer which is the year this movie came out
    
    '''
    @classmethod
    def create(self, title,imdb,duration,year):
        self.title=title
        self.imdb=imdb
        self.duration=duration
        self.year=year
    
    #might need to increase this size if there are any movies with titles larger than this
    title=models.CharField(max_length=200)#can set this as primary key
    imdb=models.CharField(max_length=500)
    duration=models.IntegerField(default=0)
    year=models.IntegerField(default=2017)#current year, might be able to switch this to time current year
    
    
    
class Review(models.Model):
    movie=models.ForeignKey(Movie,on_delete=models.CASCADE)
    text=models.CharField(max_length=500)
    score=models.IntegerField(default=0)