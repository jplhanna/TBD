from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect, HttpResponse, HttpRequest
import csv
import os

# Create your views here.
def index(request):
    return render(request, "index.html")
    
# Create your views here.
def populate(request):
    print os.getcwd()
    with open('data/movie_metadata.csv', 'rb') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in spamreader:
            print row[11]
    return render(request, "index.html")