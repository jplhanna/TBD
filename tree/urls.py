from django.conf.urls import url
from tree.views import signup,signin

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^question$', views.questions.as_view(), name='index'),
    url(r'^handleQuestion$', views.handleQuestion, name='handleQuestion'),
    url(r'^handleResponse$', views.handleResponse, name='handleResponse'),
    url(r'^handleSignUp$', views.handleSignUp, name='handleSignUp'),
    url(r'^handleSignIn$', views.handleSignIn, name='handleSignIn'),
    url(r'^handleSignOut$', views.handleSignOut, name='handleSignOut'),
    url(r'^movie/(?P<movie_id>[0-9]+)/$', views.getMovie.as_view(), name='handleQuestion'),
    url(r'^signup/', signup),
    url(r'^signin/', signin),
]