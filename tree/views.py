from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect, HttpResponse, HttpRequest
from django.views import generic
from django.db.models.aggregates import Count
import numpy as np
import random
import json

from .models import *

#For more information on the adt's of the subclasses of ListView can be found by looking in the Django documentation

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
        str_tmp = str(pool_tmp[0].id)
        for itr in pool_tmp[1:10]:
            str_tmp += ',' + str(itr.id)
        return pool_tmp[:10], str_tmp
        
    '''
    getQuestionsFromString: This method tries to find Questions from the Question table in the sqlite database, based on an input string which should contain at least 1
                            question
    input: question_string: A string which should contain 1 or more questions seperated by ,s. All of which should be in the Questions table of the sqlite database.
    output: A list containing the Question objects in order corresponding to the string of questions input
    throws: A DoesNotExist exception if any of the questions in the string do not exist in the Questions table
            A MultipleObjectsReturned if a Question being querried for occurs more than once in the Questions table
    '''
    def getQuestionsFromString(self, questions_string):
        print questions_string
        questions_string = questions_string.split(',')
        questions_tmp = []
        for itr in questions_string:
            questions_tmp.append(Question.objects.get(id=int(itr)))
        return questions_tmp
        
    '''
    get_queryset: Querries for the entire Questions table from the sqlite server
    output: A list of Question objects
    '''
    def get_queryset(self):
        return Question.objects.all()
        
    '''
    get_context_data: Used to set up the order in which questions will be asked, and preparing the scoring system. This also saves the current question session, for users.
    input: kwargs: Is a dictionary used by django for command inputs. Should be empty.
    output: context: A dictionary containing a list of questions under the key question_list, a corresponding list of the current scores for questions to movies
                     under the key scores
    modifies: Creates a new session if one does not exist for the current user.
              Creates self.request.session.scores if it doesnt not exist already, or sets them all to 0 if the last item in the scores list is 0.
              self.request.session.questions to be the current list of questions left to be answered.
    '''
    def get_context_data(self, **kwargs):
        context = super(questions, self).get_context_data(**kwargs)
        scores_str = '0,0,0,0,0,0,0,0,0,0'
        if self.request.session.session_key == None:
            self.request.session.create()
        if 'scores' not in self.request.session or self.request.session.__getitem__('scores')[-1] != '0':
            self.request.session.__setitem__('scores', scores_str)
        current_scores = self.request.session.__getitem__('scores')
        if current_scores[0] != '0' and current_scores[-1] == '0':
            print "YOU FUCKER I KNEW IT", current_scores
            context['question_list'] = self.getQuestionsFromString(self.request.session.__getitem__('questions'))
            context['scores'] = current_scores
            return context
        context['question_list'], str = self.getQuestions()
        context['scores'] = current_scores
        self.request.session.__setitem__('questions', str)
        print "...SORRY TO HAVE DOUBTED YOU"
        return context
        
        
'''
handleQuestion: Handles the users interactions with questions: outputing questions, collecting the answer and updating the session,
                eventually outputting the recommended movie
input: request: An html request which is sent by the user as they are on the Question webpage
ouput: An http_response which contains the movie object and other needed information.
'''
def handleQuestion(request):
    response_data = {}
    if request.method == "GET":
        finish = request.GET.get('finish')
        question = int(request.GET.get('q'))
        answer = request.GET.get('a')
        array = request.session.__getitem__('scores').split(',')
        array[question] = str(answer)
        str_tmp = array[0]
        for itr in array[1:]:
            str_tmp += ',' + itr
        request.session.__setitem__('scores', str_tmp)
        print request.session.__getitem__('scores')
        if question == 9 or finish == 'true':
            movies = Movie.objects.all()
            scores = [float(0)] * len(movies)
            questions = request.session.__getitem__('questions').split(',')
            for itr in range(0, len(array)):
                if int(array[itr]) == 0:
                    return
                choices = Score.objects.filter(question_id=int(questions[itr])).all()
                for choice in choices:
                    scores[choice.movie_id - 1] += float(array[itr]) * float(choice.score)
            scores = np.matrix(scores)
            response_data['best_movie'] = movies[np.argmax(scores)].id
        

        response_data['result'] = 'Create post successful!'

        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )

'''
getMovie: A class used to return the movie found by the questions, and to be recommended to the user.
'''
class getMovie(generic.ListView):
    template_name = 'movie.html'
    context_object_name = 'question_list'
    
    '''
    get_queryset: A method which returns the entire Movies table from the sqlite database
    output: A list containing Movie objects
    '''
    def get_queryset(self):
        return Movie.objects.all()
        
    '''
    get_context_data: Handles returning 
    input: A dictionary used by django to represent command options, should be empty.
    output: A dictionary containing the movie to be recommended to the user, under the key movie
    modifies: The current session data, so that the session is aware of what movie was recommended for the user.
    throws: 404 error if the movie being recommended dne in the Movies table.
    '''
    def get_context_data(self, **kwargs):
        context = super(getMovie, self).get_context_data(**kwargs)
        context['movie'] = get_object_or_404(Movie, id=int(self.kwargs["movie_id"]))
        return context
    
def signup(request):
    return render(request, "signup.html")
    
def signin(request):
    return render(request, "signin.html")
