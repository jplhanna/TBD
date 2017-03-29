from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect, HttpResponse, HttpRequest
from django.views import generic
from django.db.models.aggregates import Count
import random

from .models import *

# Create your views here.
def index(request):
    return render(request, "index.html")
    
'''
questions: A subclass of the ListView class, which is used on by question html(webpage). The class handles the collection, choosing, and presentation of questions
           given to the user during a run of the application. This class also interacts with the Questions table of the sqlite database. The questions then interacts
           with the scores and movies table.
'''
class questions(generic.ListView):
    template_name = 'question.html'
    context_object_name = 'question_list'
    
    '''
    getQuestions: Returns 10 random question from the entire Questions table from the sqlite database
    output: A pair containing a list of 10 random Question objects, and string of said questions
    '''
    def getQuestions(self):
        pool_tmp = list( Question.objects.all() )
        random.shuffle( pool_tmp )
        str_tmp = '[' + str(pool_tmp[0].id)
        for itr in pool_tmp[1:10]:
            str_tmp += ',' + str(itr.id)
        str_tmp += ']'
        return pool_tmp[:10], str_tmp
        
    '''
    getQuestionsFromString: This method tries to find Questions from the Question table in the sqlite database, based on an input string which should contain at least 1
                            question
    input: question_string: A string which should contain 1 or more questions seperated by ,s. All of which should be in the Questions table of the sqlite database.
    output: A list containing the Question objects in order corresponding to the string of questions input
    throws: A DoesNotExist exception if any of the questions in the string do not exist in the Questions table
    '''
    def getQuestionsFromString(self, questions_string):
        print questions_string
        questions_string = questions_string[1:-1].split(',')[:10]
        questions_tmp = []
        for itr in questions_string:
            questions_tmp.append(Question.objects.get(id=int(itr)))
        return questions_tmp
        
    
    def get_queryset(self):
        return Question.objects.all()
    def get_context_data(self, **kwargs):
        context = super(questions, self).get_context_data(**kwargs)
        scores = '[0,0,0,0,0,0,0,0,0,0]'
        if self.request.session.session_key == None:
            self.request.session.create()
            self.request.session.__setitem__('scores', scores)
        if 'scores' not in self.request.session:
            self.request.session.__setitem__('scores', scores)
        current_scores = self.request.session.__getitem__('scores')
        if current_scores[1] != '1' and current_scores[-2] == '0':
            context['question_list'] = self.getQuestionsFromString(self.request.session.__getitem__('questions'))
            return context
        context['question_list'], str = self.getQuestions()
        self.request.session.__setitem__('questions', str)
        return context
        
def signup(request):
    return render(request, "signup.html")
def signin(request):
    return render(request, "signin.html")
