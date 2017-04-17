from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect, HttpResponse, HttpRequest
from django.views import generic
from django.db.models.aggregates import Count
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.core.mail import send_mail
import numpy as np
import random
import json
import emailHandler as eH_tmp
emailHandler=eH_tmp.emailHandler()

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
            context['question_list'] = self.getQuestionsFromString(self.request.session.__getitem__('questions'))
            context['scores'] = current_scores
            return context
        context['question_list'], str = self.getQuestions()
        context['scores'] = current_scores
        self.request.session.__setitem__('questions', str)
        self.request.session.__setitem__('response', '0')
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
handleResponse: Handles the users interactions with questions: outputing questions, collecting the answer and updating the session,
                eventually outputting the recommended movie
input: request: An html request which is sent by the user as they are on the Question webpage
ouput: An http_response which contains the movie object and other needed information.
'''
def handleResponse(request):
    response_data = {}
    if request.method == "GET":
        response = request.GET.get('like')
        current_response = int(request.session.__getitem__('response'))
        movie = int(request.GET.get('movie'))
        multiplier = float(1 * response)
        if response == current_response:
            return
        elif current_response != 0:
            multiplier = float(2 * response)
        scores = request.session.__getitem__('scores').split(',')
        questions = request.session.__getitem__('questions').split(',')
        for itr in range(0, 10):
            score = int(scores[itr])
            if score == 0:
                return
            score_obj = get_object_or_404(Score, movie_id=movie, question_id=int(questions[itr]))
            score_obj.score += multiplier * float(.05) * float(score)
            score_obj.save()

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
    
def forgotpassword(request):
    return render(request, "forgotpassword.html")
    
'''
handleSignUp: Handles the user inputting and email and password into the input boxes on the SignUp webpage for the TBD website.
input: request: An html request which is sent by the user as they are on the SignUp webpage
output: redirects the user to the TBD front page
'''
def handleSignUp(request):
    email_tmp=request.POST['inputEmail']
    password_tmp=request.POST.get('inputPassword')
    if(User.objects.filter(username=email_tmp).exists()):
        return redirect('/tbd/signup')
    new_user=User.objects.create_user(email_tmp,email_tmp,password_tmp)
    new_user.save()
    aut_login_temp=authenticate(username=email_tmp, password=password_tmp)
    login(request,aut_login_temp)
    emailHandler.emailNewUser(email_tmp)
    return redirect('/tbd/')
    
'''
password_change: A class used to aid change_password in changing the user's password.
'''
class password_change(generic.ListView):
    
    '''
    get_context_data: a method used to retrieve contextual data for the current webpage. Specifically used when the user is asking to change their password.
    input: kwargs: Is a dictionary used by django for command inputs. Should be empty.
    output: context: a Dictionary containg the key 'email' which maps to the email connected to the current user
    '''
    def get_context_data(self,**kwargs):
        context=super(password_change,self).get_context_data(**kwargs)
        context['email']=get_object_or_404(User,id=int(self.kwargs['email_id']))
        return context
   

def handlePasswordChange(request):
    user_name_tmp=request.POST.get('email')
    old_pass_tmp=request.POST.get('old_password')
    old_pass_matches_tmp=authenticate(username=user_name_tmp, password=old_pass_tmp)
    if(old_pass_matches_tmp is None):
        return None #should redirect the user back to their settings page, once that page has been made.
    new_pass_tmp=request.POST.get('new_password')
    user_tmp=User.objects.get(user_name_tmp)
    user_tmp.set_password(new_pass_tmp)
    user_tmp.save()
    #should probably either return a success state or redirect the user back to their settings page

'''
handleForgotPassword: The method called when a user signifies that they forgot their password on the signin page.
input: request: An html request which is sent by the user as they are on the SignIn webpage
output: a redirect call which send the user back to the SignIn webpage
'''
def handleForgotPassword(request):
    user_name_tmp=request.POST.get('email')
    emailHandler.emailForgPass(user_name_tmp)
    return redirect('/tbd/signin')
    
    
    
'''
handleSignIn: The method called when a user attemps to sign in.
input: request: An html request which is sent by the user as they are on the SignIn webpage
output: a redirect call which will either send the user to the front page if the credentials are correct, or back to the signin page if not 
'''
def handleSignIn(request):
    email_tmp=request.POST.get('inputEmail')
    password_tmp=request.POST.get('inputPassword')
    is_user_tmp=authenticate(username=email_tmp,password=password_tmp)
    if(is_user_tmp is not None):
        login(request,is_user_tmp)
        return redirect('/tbd/')
    else:
        return redirect('/tbd/signin')

'''
handleSignOut: The method called when a user attempts to sign out.
input: request: An html request which is sent by the user when on page within the TBD application, while they are logged in.
output: A redirect call that send the user back to the front page 
'''
def handleSignOut(request):
    logout(request)
    return redirect('/tbd/')