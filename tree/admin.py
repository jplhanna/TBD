from django.contrib import admin

from .models import Movie, Question, Score, UserData

# Register your models here.
#List of models that can appear in the admin portion of the Delphi website

admin.site.register(Movie)
admin.site.register(Question)
admin.site.register(Score)
admin.site.register(UserData)