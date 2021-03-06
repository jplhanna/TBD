from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

#None of the classes are described in ADT form due to how basic they are, especially due to their implementaion of the django model class.
#For more information about the model class, look into the django 1.9 documentations

'''
Movie: A class used by the websites sqlite database to create the template for the corresponding table
In this case it contains all of the basic used data for movies, including what services the movie can be found on
'''
class Movie(models.Model):
    
    #might need to increase this size if there are any movies with titles larger than this
    title = models.CharField(max_length=200)#can set this as primary key
    imdb = models.CharField(max_length=500)
    popularity = models.FloatField(default=0)
    poster = models.CharField(max_length=500, default="")
    hulu = models.BooleanField(default=False)
    amazon = models.BooleanField(default=False)
    amazonPrime = models.BooleanField(default=False)
    googlePlay = models.BooleanField(default=False)
    itunes = models.BooleanField(default=False)
    netflix = models.BooleanField(default=False)
    
    '''
    __str__: a simple function usually called by the admin portion of the website, allowing it to represent the objects by something other than class_title object
    output: self.title: The string which represents the movie objects title
    '''
    def __str__(self):
        return self.title
    
'''
Question: A class used by the websites sqlite database to create the template for the corresponding table
In this case it contains a question which is used by the Delphi website.
'''
class Question(models.Model):
    question_text = models.CharField(max_length=500, unique=True)
     
    '''
    __str__: a simple function usually called by the admin portion of the website, allowing it to represent the objects by something other than class_title object
    output: self.question_text: The string which represents the question objects text
    '''
    def __str__(self):
        return self.question_text
   
'''
Score: A class used by the websites sqlite database to create the template for the corresponding table
In this case  it contains the weight between a question and a movie.
''' 
class Score(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, null=False)
    score = models.FloatField(default=0)
    
'''
Review: A class used by the websites sqlite database to create the template for the corresponding table.
In this case it contains a review a user may make for a movie.
'''
class Review(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    questions = models.CharField(max_length=100)
    score = models.IntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField()
    
    
'''
UserData: A class used by the websites sqlite database to create the template for the corresponing data.
In this case it connects a django user to user data.
'''
class UserData(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    showAll = models.BooleanField(default=True)
    hulu = models.BooleanField(default=False)
    amazon = models.BooleanField(default=False)
    amazonPrime = models.BooleanField(default=False)
    googlePlay = models.BooleanField(default=False)
    itunes = models.BooleanField(default=False)
    netflix = models.BooleanField(default=False)
    
    '''
    __str__: a simple function usually called by the admin portion of the website, allowing it to represent the objects by something other than class_title object
    output: self.user.username: The string which represents the username of the user whose data this object corresponds to.
    '''
    def __str__(self):
        return self.user.username
    
'''
UserFavorites: A class used by the websites sqlite database to create for the corresponding data.
In this case it connects a django user to a movie, which the user wishes to save.
'''
class UserFavorites(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

'''
UserFavorites: A class used by the websites sqlite database to create for the corresponding data.
In this case it connects a django user to a movie, which the user has previously been recommended.
'''
class UserRecommended(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField()

'''
UserData: A class used by the websites sqlite database to create the template for the corresponing data.
In this case it connects a django user to a random key which is used when they wish to reset their password.
'''
class ForgotPass(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    random = models.CharField(max_length=500)