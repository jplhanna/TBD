from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

#None of the classes are described in ADT form due to how basic they are, especially in their implementaion of the models class
#For more information about the model class, look into the django 1.9 documentations

'''
Movie: A class used by the websites sqlite database to create the template for the corresponding table
Contains all of the basic used data for movies
'''
class Movie(models.Model):
    
    #might need to increase this size if there are any movies with titles larger than this
    title=models.CharField(max_length=200)#can set this as primary key
    imdb=models.CharField(max_length=500)
    popularity=models.FloatField(default=0)
    poster=models.CharField(max_length=500, default="")
    hulu=models.BooleanField(default=False)
    amazon=models.BooleanField(default=False)
    amazonPrime=models.BooleanField(default=False)
    googlePlay=models.BooleanField(default=False)
    itunes=models.BooleanField(default=False)
    netflix=models.BooleanField(default=False)
    
    '''
    __unicode__: a simple function usually called by the admin portion of the website, allowing it to represent the objects by something other than class_title object
    output: self.title: The string which represents the movie objects title
    '''
    def __unicode__(self):
        return self.title
    
'''
Question: A class used by the websites sqlite database to create the template for the corresponding table
Contains a question which is used by the Delphi website
'''
class Question(models.Model):
    question_text=models.CharField(max_length=500, unique=True)
     
    '''
    __unicode__: a simple function usually called by the admin portion of the website, allowing it to represent the objects by something other than class_title object
    output: self.question_text: The string which represents the question objects text
    '''
    def __unicode__(self):
        return self.question_text
   
'''
Score: A class used by the websites sqlite database to create the template for the corresponding table
Contains the weight between a question and a movie
''' 
class Score(models.Model):
    movie=models.ForeignKey(Movie,on_delete=models.CASCADE, related_name="movie")
    question=models.ForeignKey(Question, related_name="question")
    score=models.FloatField(default=0)
    
'''
Review: A class used by the websites sqlite database to create the template for the corresponding table
'''
class Review(models.Model):
    movie=models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="movie")
    questions=models.CharField(max_length=100, related_name="questions")
    score=models.IntegerField(default=0)
    user=models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")
    date=models.DateTimeField()
    
    
'''
UserData: A class used by the websites sqlite database to crea the template for the corresponing data.
In this case it connects a django user to user data.
'''
class UserData(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE, related_name="user")
    showAll=models.BooleanField(default=True)
    hulu=models.BooleanField(default=False)
    amazon=models.BooleanField(default=False)
    amazonPrime=models.BooleanField(default=False)
    googlePlay=models.BooleanField(default=False)
    itunes=models.BooleanField(default=False)
    netflix=models.BooleanField(default=False)
    
    def __unicode__(self):
        return self.user.username
    
class UserFavorites(models.Model):
    movie=models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="movie")
    user=models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")
#NEED TO ACTUALLY MIGRATE THIS CLASS, WAITING FOR STREAMING DATA TO BE AVAILABLE
#AS WELL AS DECIDING ON HOW TO SAVE MOVIE TO THE USER

class ForgotPass(models.Model):
    username=models.CharField(max_length=500)
    random=models.CharField(max_length=500)
    