from django.conf.urls import url
from tree.views import signup,signin

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^question$', views.questions.as_view(), name='index'),
    url(r'^handleQuestion$', views.handleQuestion, name='handleQuestion'),
    url(r'^signup/', signup),
    url(r'^signin/', signin),
]