import requests
import io
import os
from bs4 import BeautifulSoup


def save_movie_review(link,target_name,total_page):
    payload = {}
    path=os.getcwd()
    fileHandle = io.open(path+'/'+target_name, 'w',encoding='utf-8')
    for i in range(0,total_page+1):
        payload["start"]=str(i)
        r = requests.post(link,params=payload)
        html = r.text
        soup = BeautifulSoup(html,"lxml")
        result = soup.select('div[id="pagecontent"] div div p')
        for j in range(0, len(result)):
            fileHandle.write(result[j].getText())
    fileHandle.close()

def process_data(fread, fwrite):
    fr = io.open(fread,encoding='utf-8')
    fw = io.open(fwrite, 'w', encoding='utf-8')
    for line in fr:
        line = line.strip()
        if line!="*** This review may contain spoilers ***" or "Add another review":
            for letter in line:
                if letter.isalpha() or letter==' ':
                    letter = letter.lower()
                    fw.write(letter)
            
#save_movie_review("http://www.imdb.com/title/tt0137523/reviews","fight_club.txt",40)
path = os.getcwd()+'/Movie_Review/raw_reviews/'
#for filename in os.listdir(path):
filename = 'the_machinist.txt'
process_data(path+filename, os.getcwd()+'/Movie_Review/processed_reviews/%s'%filename)
