from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect, HttpResponse, HttpRequest

# Create your views here.
def index(request):
    return render(request, "index.html")