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
print(newVideoTitles[0])