import csv


'''
MovieParser: Method meant to parse through a csv file containing information scraped from imdb on films
input: text_File: A string which holds the location of the csv file which is going to be parsed
output: A list of tupples containing all of the important movie information which is in the csv
'''
def MovieParser(text_File):
    _movie_List=[]
    with open(text_File,'rb') as csvfile:
        _csv_tmp=csv.reader(csvfile,delimiter=',', quotechar='"')
        #could change the code so that it finds the loction of the information using the first line of the csv using indexof
        #this way we are not using magic numbers, and don't have to worry about a consistent csv format for the parser
        for _row_tmp in _csv_tmp:
            if(_row_tmp[1]=='director_name'):
                continue
            #3: duration 11: name 17: imdb link 23: year
            _row_tmp[23] = '0' + _row_tmp[23]
            _row_tmp[3] = '0' + _row_tmp[3]
            _movie_tmp=(int(_row_tmp[3]),_row_tmp[11],_row_tmp[17],int(_row_tmp[23]))#figure out the positions of the values we need, write them down
            _movie_List.append(_movie_tmp)
    return _movie_List