from django.conf.urls import url
from tree.views import signup, signin, setting2

from . import views
#This file is simply meant to contain all urls used by the Tree application of the TBD project. Aka, the Delphi Website
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^question$', views.questions.as_view(), name='index'),
    url(r'^forgotPassword$', views.forgotpassword, name='index'),
    url(r'^handleQuestion$', views.handleQuestion, name='handleQuestion'),
    url(r'^handleRandom$', views.handleRandom, name='handleRandom'),
    url(r'^handleResponse$', views.handleResponse, name='handleResponse'),
    url(r'^handleSignIn$', views.handleSignIn, name='handleSignIn'),
    url(r'^handleSignOut$', views.handleSignOut, name='handleSignOut'),
    url(r'^handleForgotPassword$', views.handleForgotPassword, name='handleForgotPassword'),
    url(r'^handleForgotPasswordChange$', views.handleForgotPasswordChange, name='handleForgotPasswordChange'),
    url(r'^handleDeleteAccount$', views.handleDeleteAccount, name='handleDeleteAccount'),
    url(r'^handleStreamingServices$', views.handleStreamingServices, name='handleStreamingServices'),
    url(r'^movie/(?P<movie_id>[0-9]+)/$', views.getMovie.as_view(), name='handleQuestion'),
    url(r'^added$', views.added, name='added'),
    url(r'^resetPassword/(?P<user_id>.+)/$', views.resetPassword.as_view(), name='resetPassword'),
    url(r'^signup/', signup),
    url(r'^signin/', signin),
    url(r'^signin2/', views.signin2, name='signin2'),
    url(r'^settings/', views.settings.as_view()),
    url(r'^settings2/', setting2)
]