#ctx stands for context: this variable is passed to the HTML

from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect, HttpResponse, HttpRequest
from django.views import generic
from django.db.models.aggregates import Count
import random

from .models import *

# Create your views here.
def index(request):
    return render(request, "index.html")
    
class questions(generic.ListView):
    template_name = 'question.html'
    context_object_name = 'question_list'
    
    def getQuestions(self):
        pool_tmp = list( Question.objects.all() )
        random.shuffle( pool_tmp )
        return pool_tmp[:10]
    def get_queryset(self):
        return Question.objects.all()
    def get_context_data(self, **kwargs):
        context = super(questions, self).get_context_data(**kwargs)
        print self.getQuestions()
        context['question_list'] = self.getQuestions()
        return context