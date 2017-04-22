from django.core.management.base import BaseCommand, CommandError
from tree.models import Movie
from parser import MovieParser

#So rather than calling the parser we call manage with a specific function line which will call this. The function should include the location of the file being added
#Parser could be called to parse the file and return the proper list. The parser could be a factory method

class Command(BaseCommand):
    help="Updates Movie table/database with data given in csv's"
    
    def add_arguments(self,parser):
        #The argument of the add_movie_data command, aka the csv file location, there should be at least 1
        parser.add_argument('csv_location',nargs=1,help='Must input one valid csv file location')
        parser.add_argument('available',nargs=1,help='Must input one availability location')
    
    '''
    CreateMovies: A method which adds movies into the database, or updates the information of currently existing movies
    input: csv: A string containing the file location with the movies to be input
    modifies: The movie table contained in db.splite3, and based on the Movie model in the Tree application. Adds movies into said database
    '''
    def CreateMovies(self, csv, available):
        _movie_Data=MovieParser(csv)
        for _movie_tmp in _movie_Data:
            _movie = Movie.objects.filter(imdb=_movie_tmp[1]).all()
            if(len(_movie) == 1):
                _new_Movie_tmp = _movie[0]
            else:
                _new_Movie_tmp=Movie(title=_movie_tmp[0],imdb=_movie_tmp[1],poster=_movie_tmp[2],popularity=_movie_tmp[4])
            if available == "amazon":
                _new_Movie_tmp.amazon = True
            elif available == "amazonPrime":
                _new_Movie_tmp.amazonPrime = True
            elif available == "googlePlay":
                _new_Movie_tmp.googlePlay = True
            elif available == "hulu":
                _new_Movie_tmp.hulu = True
            elif available == "itunes":
                _new_Movie_tmp.itunes = True
            elif available == "netflix":
                _new_Movie_tmp.netflix = True
            _new_Movie_tmp.save()
        
    '''
    handle: The command connected to the manage.py command prompt. Is meant to update/populate the movie database using a csv
    input: *args: A list of arguments which have been input. 
           **options: A map of operations, which contain options for the command which is being run. Which should just include the csv file location
    '''
    def handle(self,*args,**options):
        self.CreateMovies(options['csv_location'][0], options['available'][0])