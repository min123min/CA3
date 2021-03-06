from requests import get, post
import json
from dateutil import parser
import datetime
import requests
import lxml
import bs4
import os
GoogleDrive = "https://drive.google.com/drive/folders/1pFHUrmpLv9gEJsvJYKxMdISuQuQsd_qX"
video_titles = []
links = []
def GdriveScrape(url):
    page = requests.get(url)    
    data = page.text
    soup = bs4.BeautifulSoup(data, 'html.parser')
    videos = soup.find_all('div',class_ = 'Q5txwe')
    ###########################
    for video in videos:
        video_titles.append(video)
        links.append(video.parent.parent.parent.parent.attrs['data-id'])
    return links,video_titles
NewLinks, newVideoTitles = GdriveScrape(GoogleDrive)
lowestCount = 0
dateOne = newVideoTitles[0]["aria-label"]
i = 0
while i != 100:
    for num in newVideoTitles[i]["aria-label"]:
        if(num==" "):
            newVideoTitles[i]["aria-label"]= newVideoTitles[i]["aria-label"][:num]
            # newVideoTitles[i]["aria-label"]= newVideoTitles[i].__index__(" ")
        
    
    i +=1
print(newVideoTitles)
dateTwo

theLooped = datetime.datetime(newVideoTitles[0]["aria-label"])
secondedDate= datetime.datetime(newVideoTitles[0+1]["aria-label"])
print("d1 is greater than d2 : ", theLooped > secondedDate) 
# while i<100:
#     theLooped = datetime.datetime(newVideoTitles[i]["aria-label"])
#     secondedDate= datetime.datetime(newVideoTitles[i+1]["aria-label"])
#     if()

print(newVideoTitles[0]["aria-label"])
#print(NewLinks)
