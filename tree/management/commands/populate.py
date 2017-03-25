from django.core.management.base import BaseCommand, CommandError
from tree.models import Movie
from parser import MovieParser

#So rather than calling the parser we call manage with a specific function line which will call this. The function should include the location of the file being added
#Parser could be called to parse the file and return the proper list. The parser could be a factor method

class Command(BaseCommand):
    help="Populates Movie table/database with data given in csv's"
    
    def add_arguments(self,parser):
        #The argument of the populate command, aka the csv file location, there should be at least 1
        parser.add_argument('csv_location',nargs='+',help='Must input one valid csv file location')
    
    '''
    CreateMovies: A method which populates or adds movies into the database
    input: csv: A string containing the file location with the movies to be input
    modifies: The movie database contained in db.splite3, and based on the Movie model in the Tree application. Adds movies into said database
    '''
    def CreateMovies(self, csv):
        _movie_Data=MovieParser(csv)
        for _movie_tmp in _movie_Data:
            _new_Movie_tmp=Movie(title=_movie_tmp[1],imdb=_movie_tmp[2],duration=_movie_tmp[0],year=_movie_tmp[3])
            _new_Movie_tmp.save()
        
    '''
    handle: The command connected to the manage.py command prompt. Is meant to update/populate the movie database using a csv
    input: *args: A list of arguments which have been input. Which should just include the csv file location
           **options: A map of operations, which contain options for the command which is being run. 
    '''
    def handle(self,*args,**options):
        for _csv_tmp in options['csv_location']:
            self.CreateMovies(_csv_tmp)