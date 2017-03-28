from django.conf.urls import url
from tree.views import signup,signin

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^signup/', signup),
    url(r'^signin/', signin),
    url(r'^pop$', views.populate, name='index'),
]