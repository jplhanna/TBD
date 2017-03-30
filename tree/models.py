from __future__ import unicode_literals

from django.db import models

#None of the classes are described in ADT form due to how basic they are, especially in their implementaion of the models class
#For more information about the model class, look into the django 1.9 documentations

'''
Movie: A class used by the websites sqlite database to create the template for the corresponding table
'''
class Movie(models.Model):
    
    '''
    __str__: a simple function usually called by the admin portion of the website, allowing it to represent the objects by something other than class_title object
    output: self.title: The string which represents the movie objects title
    '''
    def __str__(self):
        return self.title
    
    #might need to increase this size if there are any movies with titles larger than this
    title=models.CharField(max_length=200)#can set this as primary key
    imdb=models.CharField(max_length=500)
    duration=models.IntegerField(default=0)
    year=models.IntegerField(default=2017)#current year, might be able to switch this to time current year
    
'''
Question: A class used by the websites sqlite database to create the template for the corresponding table
'''
class Question(models.Model):
    question_text=models.CharField(max_length=500, unique=True)
     
    '''
    __str__: a simple function usually called by the admin portion of the website, allowing it to represent the objects by something other than class_title object
    output: self.question_text: The string which represents the question objects text
    '''
    def __str__(self):
        return self.question_text
   
'''
Score: A class used by the websites sqlite database to create the template for the corresponding table
''' 
class Score(models.Model):
    movie=models.ForeignKey(Movie,on_delete=models.CASCADE)
    question=models.ForeignKey(Question, null=False)
    score=models.DecimalField(default=0, decimal_places=3, max_digits=5)
    
'''
Review: A class used by the websites sqlite database to create the template for the corresponding table
'''
class Review(models.Model):
    movie=models.ForeignKey(Movie,on_delete=models.CASCADE)
    text=models.CharField(max_length=500)
    score=models.IntegerField(default=0)
    
#Might need to add a model here, for the yes and no choices