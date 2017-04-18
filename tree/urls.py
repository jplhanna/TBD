from django.conf.urls import url
from tree.views import signup,signin

from . import views

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
    url(r'^movie/(?P<movie_id>[0-9]+)/$', views.getMovie.as_view(), name='handleQuestion'),
    url(r'^resetPassword/(?P<user_id>.+)/$', views.resetPassword.as_view(), name='resetPassword'),
    url(r'^signup/', signup),
    url(r'^signin/', signin),
    url(r'^signin2/', views.signin2, name='signin2'),
]