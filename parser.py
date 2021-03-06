import csv


'''
MovieParser: Method meant to parse through a csv file containing information scraped from imdb
             on films
input: text_File: A string which holds the location of the csv file which is going to be parsed
output: A list of tupples containing all of the important movie information which is in the csv
'''
def MovieParser(text_File):
    _movie_List = []
    with open(text_File, 'rb') as csvfile:
        _csv_tmp = csv.reader(csvfile, delimiter=',', quotechar='"')
        for _row_tmp in _csv_tmp:
            if(_row_tmp[1] == 'full_path'):
                continue
            #3: duration 11: name 17: imdb link 23: year
            _row_tmp[4] = '0' + _row_tmp[4]
            _movie_tmp = (_row_tmp[0], _row_tmp[1], _row_tmp[2], _row_tmp[3], float(_row_tmp[4]))
            _movie_List.append(_movie_tmp)
    return _movie_List