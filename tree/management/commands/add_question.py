from django.core.management.base import BaseCommand, CommandError
from tree.models import *

#So rather than calling the parser we call manage with a specific function line which will call this. The function should include the location of the file being added
#Parser could be called to parse the file and return the proper list. The parser could be a factor method

class Command(BaseCommand):
    help="Adds a question to the database"
    
    def add_arguments(self,parser):
        #The argument of the populate command, aka the csv file location, there should be at least 1
        parser.add_argument('question_text',nargs='+',help='Must input question text')
    
    '''
    CreateMovies: A method which populates or adds movies into the database
    input: csv: A string containing the file location with the movies to be input
    modifies: The movie database contained in db.splite3, and based on the Movie model in the Tree application. Adds movies into said database
    '''
    def CreateQuestion(self, question):
        if(len(question) >= 500):
            print "ERROR: Question must be under 500 characters"
            return
        _new_Question_tmp=Question(question_text=question)
        _new_Question_tmp.save()
        _movies_array_tmp = Movie.objects.all()
        for m in _movies_array_tmp:
            _new_Score_tmp=Score(movie=m, question=_new_Question_tmp, score=.5)
            _new_Score_tmp.save()
        
    '''
    handle: The command connected to the manage.py command prompt. Is meant to update/populate the movie database using a csv
    input: *args: A list of arguments which have been input. Which should just include the csv file location
           **options: A map of operations, which contain options for the command which is being run. 
    '''
    def handle(self,*args,**options):
        str = ""
        for q in options['question_text']:
            str += q + " "
        if str[-2] == '?':
            str = str[:-1]
        else:
            str = str[:-1] + '?'
        self.CreateQuestion(str)