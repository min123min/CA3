from requests import get, post
import json
from dateutil import parser
import datetime
import requests
import lxml
import bs4
import os
import numpy as np
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
print ("https://drive.google.com/file/d/"+NewLinks[0]+"/view?usp=sharing")
try:
    while newVideoTitles[i]["aria-label"] != None:
        newitem =  str(newVideoTitles[i]["aria-label"][:10])
        newVideoTitles[i]["aria-label"] =  newitem
        print(newitem)
        # for num in newVideoTitles[i]["aria-label"]:
        #     # if(num==" "):
        #     #     newVideoTitles[i]["aria-label"]= str(newVideoTitles[i]["aria-label"])[:num]
        #     newitem =  str(newVideoTitles[i]["aria-label"][:10])
        #     print(newitem)
        #     # newVideoTitles[i]["aria-label"] = datetime.datetime(np.dtype('int64').type(newitem), '%Y-%m-%d')
        #         # newVideoTitles[i]["aria-label"]= newVideoTitles[i].__index__(" ")
            
        
        i +=1
except:
    print("Error in counting")
print(newVideoTitles[1]["aria-label"])



# while i<100:
#     theLooped = datetime.datetime(newVideoTitles[i]["aria-label"])
#     secondedDate= datetime.datetime(newVideoTitles[i+1]["aria-label"])
#     if()

print(newVideoTitles[0]["aria-label"])
#print(NewLinks)
