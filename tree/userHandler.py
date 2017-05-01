from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect
from .models import *
import emailHandler as eH

'''
userHandler: a simple static class used by the views.py when doing major interactions or modifications with a Django user object

representation invariant: this._emailHandler will always equal a static instance of a emailHandler class from emailHandler.py

abstract function: None
'''
class userHandler:
    _emailHandler=eH.emailHandler()
    
    '''
    createUser: called when ever someone attempts to create a new user account, and redirects the user to a different webpage
    input: email: A string which should be a legitamite email input by the user
           password: A string containing the password the user wishes to use for their account
           confirm_password: A string containing a second input by the user to confirm their password
           request: An html request sent by the signup webpage went the user submits their information
    output: If the email is already in use or the password do not match the they are returned to the signup page with an error
            Otherwise the user is sent to their settings page
    '''
    def createUser(self, email, password, confirm_password, request):
        if(User.objects.filter(username = email).exists()):
            return render(request, "signup.html", {'error': "Email is already in use"})
        if(password==confirm_password):
            new_user=User.objects.create_user(email,email,password)
            new_user.save()
            #makes a UserData database object that is related to the user just made
            new_user_data = UserData(user = new_user)
            new_user_data.save()
            aut_login_temp = authenticate(username = email, password = password)
            login(request,aut_login_temp)
            self._emailHandler.emailNewUser(email)
            return redirect('/tbd/settings/')#Change this redirect to the settings page once it has been made
        else:
            return render(request,"signup.html", {'error':"Password didn't match"})
    
    '''
    setStreamingData: a method which is called whenever the user interacts with their streaming services on their settings page
    input: service: should contain an integer between 0 and 5, which corresponds to a streaming service
           status: A boolean which signifies whether the user is checking or unchecking that streaming service
           currUser: The django user object for the current user
    modifies: changes a streaming service boolen within the corresponding userData object for the current user
    '''
    def setStreamingData(self, service, status, currUser):
        userData = UserData.objects.filter(user=currUser)[0]
        if service == 0:
            userData.amazon = status
        elif service == 1:
            userData.amazonPrime = status
        elif service == 2:
            userData.netflix = status
        elif service == 3:
            userData.hulu = status
        elif service == 4:
            userData.itunes = status
        elif service == 5:
            userData.googlePlay = status
        if(userData.amazon == userData.amazonPrime == userData.netflix == userData.hulu ==
           userData.itunes == userData.googlePlay == False):
            userData.showAll = True
        else:
            userData.showAll = False
        userData.save()
    
    '''
    changePassword: simply changes the password for a user
    input: user: The django user object that will have its password changed
           password: A string containing the new password for the user
    modifies: Changes the password for the corresponding user
    '''
    def changePassword(self, user, password):
        user.set_password(password)
        user.save()
    
    '''
    addToFavorite: Called whenever a user wishes to add a movie to their favorites list, either from a movie info page, or their settings page
    input: request: An html request sent from the settings page, or movie info page, when a user clicks add to favorites
    output: Sends the webpage a render to give feedback the the movie was added.
    modifies: The UserFavorites sql database, by either adding or removing an object
    '''
    def addToFavorite(self, request):
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
    deleteFavorite: called when the user wishes to delete a favorite from their settings page
    input: request: an html request sent when the user clicks to delete a movie from their favorites list on their settings page
    modifies: The UserFavorites sql database, by removing an object
    '''
    def deleteFavorite(self, request):
        movie_id_tmp = request.GET.get('movie_id')
        currUser = request.user
        favorite_tmp = UserFavorites.objects.filter(user=currUser, movie_id=movie_id_tmp)
        favorite_tmp.delete()