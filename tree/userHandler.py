from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect
from .models import *
import emailHandler as eH

class userHandler:
    _emailHandler=eH.emailHandler()
    
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
            return redirect('/tbd/')#Change this redirect to the settings page once it has been made
        else:
            return render(request,"signup.html", {'error':"Password didn't match"})
            
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
    
    def changePassword(self, user, password):
        user.set_password(password)
        user.save()
    
    def addToFavotite(self, request):
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
    
    def deleteFavorite(self, request):
        movie_id_tmp = request.GET.get('movie_id')
        currUser = request.user
        favorite_tmp = UserFavorites.objects.filter(user=currUser, movie_id=movie_id_tmp)
        favorite_tmp.delete()