from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect, HttpResponse, HttpRequest
from django.views import generic
from django.db.models.aggregates import Count
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.core.mail import send_mail
import numpy as np
import tree.emailHandler as eH_tmp
from userHandler import userHandler
from datetime import datetime
from questionHandler import questionHandler

from .models import *

import random
import json

emailHandler = eH_tmp.emailHandler()
user_help = userHandler()

#For more information on the adt's of the subclasses of ListView can be found
#by looking in the Django documentation

# Create your views here.
'''
index: The method called when the user reaches the main page of the Delphi website.
input: request: An html request which is sent by the user when they try to enter the Delphi website
output: A render call using the users request and index.html, which builds the main page
'''
def index(request):
    return render(request, "index.html")

'''
signin2: The method called when the user fails to sign in due to a bad password or email.
input: request: An html request which is sent by the handleSignIn method when the user fails to sign in
output: A render call using the users original signin request and the second signin webpage, thus building that page.
'''
def signin2(request):
    return render(request, "signin2.html")
'''
questions: A subclass of the ListView class, which is used on by question html(webpage). The class handles the collection, choosing, and presentation of questions
           given to the user during a run of the application. This class also interacts with the Questions table of the sqlite database. The questions then interacts
           with the scores and movies table.
'''
class questions(generic.ListView):
    template_name = 'question.html'
    context_object_name = 'question_list'

    '''
    getQuestions: Returns 10 random question from the entire Questions table
                    from the sqlite database
    output: A pair containing a list of 10 random Question objects, and string of said questions
    '''
    def getQuestions(self):
        pool_tmp = list(Question.objects.all())
        random.shuffle(pool_tmp)
        str_tmp = str(pool_tmp[0].id)
        for itr in pool_tmp[1:10]:
            str_tmp += ',' + str(itr.id)
        return pool_tmp[:10], str_tmp

    '''
    getQuestionsFromString: This method tries to find Questions from the Question table in the
                            sqlite database, based on an input string which should contain at
                            least 1 question
    input: question_string: A string which should contain 1 or more questions seperated by ,s.
                            All of which should be in the Questions table of the sqlite database.
    output: A list containing the Question objects in order corresponding to the string of
            questions input
    throws: A DoesNotExist exception if any of the questions in the string do not exist in the
            Questions table
            A MultipleObjectsReturned if a Question being querried for occurs more than once in
            the Questions table
    '''
    def getQuestionsFromString(self, questions_string):
        print questions_string
        questions_string = questions_string.split(',')
        questions_tmp = []
        for itr in questions_string:
            questions_tmp.append(Question.objects.get(id=int(itr)))
        return questions_tmp

    '''
    get_queryset: Queries for the entire Questions table from the sqlite server
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
        if('scores' not in self.request.session or
           'finish' not in self.request.session or
           self.request.session.__getitem__('scores')[-1] != '0' or
           self.request.session.__getitem__('finish') == 1):
            self.request.session.__setitem__('scores', scores_str)
            self.request.session.__setitem__('finish', 0)
        current_scores = self.request.session.__getitem__('scores')
        if current_scores[0] != '0' and current_scores[-1] == '0':
            context['question_list'] = self.getQuestionsFromString(
                self.request.session.__getitem__('questions'))
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
        #finish = request.GET.get('finish')
        question = int(request.GET.get('q'))
        answer = request.GET.get('a')
        print "ans", answer
        array = request.session.__getitem__('scores').split(',')
        array[question] = str(answer)
        str_tmp = array[0]
        for itr in array[1:]:
            str_tmp += ',' + itr
        request.session.__setitem__('scores', str_tmp)
        print "important", request.session.__getitem__('scores')
        if question == 9 or answer == '0':
            if str_tmp == "0,0,0,0,0,0,0,0,0,0":
                return handleRandom(request)
            currUser = request.user
            questions = request.session.__getitem__('questions').split(',')
            q_help_tmp = questionHandler(currUser)
            best_movie = q_help_tmp.getBestMovie(array, questions)
            response_data['best_movie'] = best_movie.id
            if currUser.username != "":
                _recommend_tmp = UserRecommended.objects.filter(user=request.user, movie=best_movie)
                if _recommend_tmp.exists():
                    _recommend_tmp = UserRecommended.objects.filter(user=request.user,
                                                                    movie=best_movie).all()[0]
                    _recommend_tmp.date = datetime.now()
                else:
                    _recommend_tmp = UserRecommended(user=request.user,
                                                     movie=best_movie, date=datetime.now())
                _recommend_tmp.save()
            request.session.__setitem__('finish', 1)
            handleRandom(request)
            #response_data['best_movie'] = best_movie.id

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
            return HttpResponse(
                json.dumps(response_data),
                content_type="application/json"
            )
        elif current_response != 0:
            multiplier = float(2 * response)
        scores = request.session.__getitem__('scores').split(',')
        questions = request.session.__getitem__('questions').split(',')
        for itr in range(0, 10):
            score = int(scores[itr])
            if score == 0:
                return HttpResponse(
                    json.dumps(response_data),
                    content_type="application/json"
                )
            score_obj = get_object_or_404(Score, movie_id=movie,
                                          question_id=int(questions[itr]))
            score_obj.score += multiplier * float(.05) * float(score)
            score_obj.save()
        response_data['result'] = 'Create post successful!'

        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )

'''
handleRandom: Handles the user pressing the random movie button which exists on the front page of the Delphi website
input: request: An html request which is sent by the user as they are on the front page through the random button
output: Redirects the user to a random movie info page
'''
def handleRandom(request):
    total_movies_tmp = Movie.objects.count()-1
    rand_movie_index_tmp = random.randint(0, total_movies_tmp)
    return redirect('/tbd/movie/' + str(rand_movie_index_tmp) + '/')

'''
getMovie: A class used to return a movie found by the questions or the random button, and to be recommended to the user.
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


'''
added: A method used when the user asks to add a movie to their favorites list\
input: request: An html request when the user presses the add to favorites button on a movie info page
output: redirect the user to the signin page if they are not logged index
modifies: Changes the UserFavorites table by adding a new UserFavorites object which corresponds to the current user and the movie they wished to add.
'''
def added(request):
    response_data = {}
    if request.user.username == "":
        return redirect('/tbd/signin')
    if request.method == "GET":
        return user_help.addToFavorite(request)
        '''
        movie_id = int(request.GET.get('movie_id'))
        movie = Movie.objects.filter(id=movie_id).all()[0]
        if int(request.GET.get('add')) == 1:
            if UserFavorites.objects.filter(user=request.user, movie=movie).exists():
                return render(request, "added.html")
            userFav = UserFavorites(user=request.user, movie=movie)
            userFav.save()
            return render(request, "added.html")
        else:
            fav = UserFavorites.objects.filter(user=request.user, movie=movie)
            if UserFavorites.objects.filter(user=request.user, movie=movie).exists():
                fav.delete()
            response_data['result'] = 'Create post successful!'

            return HttpResponse(
                json.dumps(response_data),
                content_type="application/json"
            )
        '''
    return render(request, "added.html")
'''
signup: Handles the user inputting and email and password into the input boxes on the SignUp webpage for the TBD website.
input: request: An html request which is sent by the user as they are on the SignUp webpage
output: If the user is already signed in or successfully signs up they are signed into the Delphi homepage
        Otherwise they are sent back to the signup page, signifying the email is in use, if that was the issue
modifies: The Django user database by creating a new user object
          The UserData table in the Django sqlite database by creating a corresponing UserData object for the new user
'''
def signup(request):
    if request.user.username == "":
        if request.method == "POST":
            email_tmp = request.POST['inputEmail']
            password_tmp = request.POST.get('inputPassword')
            confirm_tmp = request.POST.get('inputPass')
            return user_help.createUser(email_tmp, password_tmp, confirm_tmp, request)
            '''
            if(User.objects.filter(username = email_tmp).exists()):
                return render(request, "signup.html", {'error': "Email is already in use"})
            if(password_tmp==confirm_tmp):
                new_user=User.objects.create_user(email_tmp,email_tmp,password_tmp)
                new_user.save()
                #makes a UserData database object that is related to the user just made
                new_user_data = UserData(user = new_user)
                new_user_data.save()
                aut_login_temp = authenticate(username = email_tmp, password = password_tmp)
                login(request,aut_login_temp)
                emailHandler.emailNewUser(email_tmp)
                return redirect('/tbd/')
                #Change this redirect to the settings page once it has been made
            else:
                return render(request,"signup.html", {'error':"Password didn't match"})
            '''
        return render(request, "signup.html")
    else:
        return redirect('/tbd')

'''
signin: A method called when a user clicks the signin button on any Delphi webpage.
input: request: An html request which is sent when a user presses the signin button on the Delphi navigation bar
output: If the user is somehow already logged in, they are sent back to the Delphi homepage.
        Otherwise the user is sent to the signin webpage
'''
def signin(request):
    if request.user.username == "":
        return render(request, "signin.html")
    else:
        return redirect('/tbd')

'''
forgotpassword: A method called when the user wishes to reset their password because they forgot it, while trying to log in
input: request: An html request which is sent when the user presses the forgot password button on the signin webpage
output: If the user is somehow already logged in, they are sent back to the Delphi homepage.
        Otherwise the user is sent to the forgotpassword webpage
'''
def forgotpassword(request):
    if request.user.username == "":
        return render(request, "forgotPassword.html")
    else:
        return redirect('/tbd')

'''
password_change: A class used to aid change_password in changing the user's password.
'''
class password_change(generic.ListView):

    '''
    get_context_data: a method used to retrieve contextual data for the current webpage.
                        Specifically used when the user is asking to change their password.
    input: kwargs: Is a dictionary used by django for command inputs. Should be empty.
    output: context: a Dictionary containg the key 'email' which maps to the email connected
                        to the current user
    '''
    def get_context_data(self, **kwargs):
        context = super(password_change, self).get_context_data(**kwargs)
        context['email'] = get_object_or_404(User, id=int(self.kwargs['email_id']))
        return context

'''
handleForgotPasswordChange: A method called from the unique webpage used when a user forgets their password and requests to change it.ArithmeticError
input: request: AN html request sent from the changed forgotten password webpage.

currently not fully functional
'''
def handleForgotPasswordChange(request):
    new_pass_tmp = request.POST.get('inputPassword')
    random = request.POST.get('submit')
    check = get_object_or_404(ForgotPass, random=random)
    user_tmp = get_object_or_404(User, username=check.username)
    user_help.changePassword(user_tmp, new_pass_tmp)
    '''
    user.set_password(new_pass_tmp)
    user.save()
    '''
    check.delete()
    return redirect('/tbd/signin')

'''
handlePasswordChange: A method called when the user tries to change their password from their settings page
input: request: An html request which is sent by the user when they try change their password from the settings webpage
output: Will only send a redirect back to the settings page if the password change fails
'''
def handlePasswordChange(request):
    user_name_tmp = request.user.username
    old_pass_tmp = request.POST.get('old_password')
    old_pass_matches_tmp = authenticate(username=user_name_tmp, password=old_pass_tmp)
    if old_pass_matches_tmp is None:
        return redirect('/tbd/settings/') #should redirect the user back to settings page
    new_pass_tmp = request.POST.get('new_password')
    user_tmp = User.objects.get(user_name_tmp)
    user_help.changePassword(user_tmp, new_pass_tmp)
    '''
    user_tmp.set_password(new_pass_tmp)
    user_tmp.save()
    '''

'''
handleForgotPassword: The method called when a user signifies that they forgot their password on the signin page.
input: request: An html request which is sent by the user as they are on the SignIn webpage
output: a redirect call which send the user back to the SignIn webpage
'''
def handleForgotPassword(request):
    user_name_tmp = request.POST.get('email')
    user_tmp = get_object_or_404(User, username=user_name_tmp)
    random_url = ""
    # if ForgotPass.objects.filter(user=user_tmp).exists():
    #     random_url = ForgotPass.objects.filter(user=user_tmp).all()[0].random
    # else:
    for count_tmp in range(1, 10):
        for itr in range(0, 5 * count_tmp):
            tmp = int(random.random()*62)
            if tmp < 10:
                random_url += str(tmp)
            elif tmp < 36:
                random_url += chr(tmp + 55)
            else:
                random_url += chr(tmp + 61)
        if not ForgotPass.objects.filter(random=random_url).exists():
            break
        else:
            random_url = ""
    if random_url == "":
        return redirect('/tbd/forgotPassword')
    forgotpass_tmp = ForgotPass(user=user_tmp, random=random_url)
    forgotpass_tmp.save()
    emailHandler.emailForgPass(user_name_tmp, random_url)
    return redirect('/tbd/signin')


'''
resetPassword: A class used to aid handleForgotPassword in changing the user's password.
'''
class resetPassword(generic.ListView):
    template_name = 'resetPassword.html'
    context_object_name = 'question_list'

    '''
    get_queryset: A method which returns the entire Movies table from the sqlite database
    output: A list containing Movie objects
    '''
    def get_queryset(self):
        return UserFavorites.objects.all()

    '''
    get_context_data: a method used to retrieve contextual data for the current webpage.
                        Specifically used when the user is asking to change their password.
    input: kwargs: Is a dictionary used by django for command inputs. Should be empty.
    output: context: a Dictionary containg the key 'email' which maps to the email connected
                        to the current user
    '''
    def get_context_data(self, **kwargs):
        context = super(resetPassword, self).get_context_data(**kwargs)
        context['random'] = self.kwargs["user_id"]
        return context


'''
handleSignIn: The method called when a user attemps to sign in.
input: request: An html request which is sent by the user as they are on the SignIn webpage
output: a redirect call which will either send the user to the front page if the credentials are
        correct, or back to the signin page if not 
'''
def handleSignIn(request):
    email_tmp = request.POST.get('inputEmail')
    password_tmp = request.POST.get('inputPassword')
    is_user_tmp = authenticate(username=email_tmp, password=password_tmp)
    if is_user_tmp is not None:
        login(request, is_user_tmp)
        return redirect('/tbd/')
    else:
        return redirect('/tbd/signin2')

'''
handleSignOut: The method called when a user attempts to sign out.
input: request: An html request which is sent by the user when on page within the TBD application, while they are logged in.
output: A redirect call that send the user back to the front page 
'''
def handleSignOut(request):
    logout(request)
    return redirect('/tbd/')


'''
settings: A class used to show user their settings while they are on their settings page.
'''
class settings(generic.ListView):
    template_name = 'settings.html'
    context_object_name = 'question_list'

    '''
    get_queryset: A method which returns the entire Movies table from the sqlite database
    output: A list containing Movie objects
    '''
    def get_queryset(self):
        return UserFavorites.objects.all()

    '''
    get_context_data: a method used to retrieve contextual data for the current webpage. Specifically used when the user is asking to change their password.
    input: kwargs: Is a dictionary used by django for command inputs. Should be empty.
    output: context: a Dictionary containg the key 'favorites' which maps to a list of favorited movies connected to the current user,
                     as well as a key for each streaming service, which maps to a boolean that signifies whether that service checked off or not
    modifies: In the rare case that the user did not have a corresponding UserData object in the sqlite database, that object is created and saved.
    '''
    def get_context_data(self, **kwargs):
        _fav_movie_array_tmp = []
        _prev_movie_array_tmp = []
        if self.request.user.username == "":
            return redirect('/tbd/signin')
        context = super(settings, self).get_context_data(**kwargs)
        for m in UserFavorites.objects.filter(user=self.request.user).all():
            _fav_movie_array_tmp.append(m.movie)
        for m in UserRecommended.objects.filter(user=self.request.user).all().order_by('-date'):
            _prev_movie_array_tmp.append(m.movie)
        context['favorites'] = _fav_movie_array_tmp
        context['previous'] = _prev_movie_array_tmp
        currUser = self.request.user
        userData = UserData.objects.filter(user=currUser).all()
        if len(userData) < 1:
            userData = UserData(user=currUser)
            userData.save()
        else:
            userData = userData[0]
        context['amazon'] = userData.amazon
        context['amazonPrime'] = userData.amazonPrime
        context['netflix'] = userData.netflix
        context['hulu'] = userData.hulu
        context['itunes'] = userData.itunes
        context['googlePlay'] = userData.googlePlay
        return context



'''
handleStreamingServices: A method which handles saving users streaming services. It is called every time a user checks or unchecks a service on their settings page
input: request: An html request which is sent by the user when on page within the TBD webpage, while they are using their settings page.
Output: An HttpResponse used to verify that the method successfully ran
modifies: The UserData table in the Django sqlite database. Specifically the UserData connected to the currently logged in user.
'''
def handleStreamingServices(request):
    response_data = {}
    if request.method == "GET":
        service = int(request.GET.get('service'))
        onOff = request.GET.get('toggle') == 'true'
        currUser = request.user
        user_help = userHandler()
        user_help.setStreamingData(service, onOff, currUser)
        '''
        userData = UserData.objects.filter(user=currUser)[0]
        print onOff == 'true'
        if service == 0:
            userData.amazon = onOff
        elif service == 1:
            userData.amazonPrime = onOff
        elif service == 2:
            userData.netflix = onOff
        elif service == 3:
            userData.hulu = onOff
        elif service == 4:
            userData.itunes = onOff
        elif service == 5:
            userData.googlePlay = onOff
        if(userData.amazon == userData.amazonPrime == userData.netflix == userData.hulu ==
           userData.itunes == userData.googlePlay == False):
            userData.showAll = True
        else:
            userData.showAll = False
        userData.save()
        '''

        response_data['result'] = 'Create post successful!'

        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )

'''
handleDeleteAccount: A method which is called when the user wishes to delete their account.
input: request: An html request sent when the user confirms they want to delete their account
                on their settings page
output: The user is redirected back to the Delphi front page, if they were somehow not logged
        in they are instead sent to signin page
modifies: If the user is logged in, their account is deleted from the django database. All
          connected objects in the sqlite database are automatically deleted.
'''
def handleDeleteAccount(request):
    currUser = request.user
    if currUser.username == "":
        return redirect("/tbd/signin")
    else:
        currUser.delete()
        return redirect("/tbd")

'''
handleDeleteFavorite: A method called when the user wishes to delete a movie from their favorites.
input: request: An html request sent when the user clicks the delete button on their favorites list
output: An HttpResponse used to verify that the method successfully ran.
modifies: The favorites table in the slqite database, the corresponding movie is removed.
'''
def handleDeleteFavorite(request):
    response_data = {}
    if request.method == "GET":
        '''
        movie_id_tmp = request.GET.get('movie_id')
        currUser = request.user
        favorite_tmp = UserFavorites.objects.filter(user=currUser, movie_id=movie_id_tmp)
        favorite_tmp.delete()
        '''
        user_help = userHandler()
        user_help.deleteFavorite(request)

        response_data['result'] = 'Delete successful!'

        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )


def setting2(request):
    return render(request,"settings2.html")