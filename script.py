from requests import get, post
import json
from dateutil import parser
import datetime
import requests
import lxml
from bs4 import BeautifulSoup
import bs4
import os
import numpy as np

# this is what is needed to grab ever thing needed 
GoogleDrive = "https://drive.google.com/drive/folders/1pFHUrmpLv9gEJsvJYKxMdISuQuQsd_qX"
courseid = "34"
KEY = "8cc87cf406775101c2df87b07b3a170d"
URL = "https://034f8a1dcb5c.eu.ngrok.io"
ENDPOINT = "/webservice/rest/server.php"
video_titles = []
links = []
#this grabs the url for the videos
def GdriveScrape(url):
    page = requests.get(url)    
    data = page.text
    soup = bs4.BeautifulSoup(data, 'html.parser')
    videos = soup.find_all('div',class_ = 'Q5txwe')
    for video in videos:
        video_titles.append(video)
        links.append(video.parent.parent.parent.parent.attrs['data-id'])
    return links,video_titles
NewLinks, newVideoTitles = GdriveScrape(GoogleDrive)

class LocalUpdateSections(object):
    def __init__(self, cid, sectionsdata):
        self.updatesections = call(
            'local_wsmanagesections_update_sections', courseid=cid, sections=sectionsdata)
            
def call(fname, **kwargs):
    parameters = rest_api_parameters(kwargs)
    parameters.update(
        {"wstoken": KEY, 'moodlewsrestformat': 'json', "wsfunction": fname})
    response = post(URL + ENDPOINT, data=parameters).json()
    if type(response) == dict and response.get('exception'):
        raise SystemError("Error calling Moodle API\n", response)
    return response

def rest_api_parameters(in_args, prefix='', out_dict=None):
    if out_dict is None:
        out_dict = {}
    if not type(in_args) in (list, dict):
        out_dict[prefix] = in_args
        return out_dict
    if prefix == '':
        prefix = prefix + '{0}'
    else:
        prefix = prefix + '[{0}]'
    if type(in_args) == list:
        for idx, item in enumerate(in_args):
            rest_api_parameters(item, prefix.format(idx), out_dict)
    elif type(in_args) == dict:
        for key, item in in_args.items():
            rest_api_parameters(item, prefix.format(key), out_dict)
    return out_dict

# get the folder
def FolderSystem():
    global FileSystem
    FileSystem = next(os.walk('.'))[1]
    del FileSystem[-1]  
    FileSystem.pop(0)  
    


FolderSystem()  
global directorycounter
directorycounter = 1
try:
    for x in FileSystem:
        dir_name = 'wk' + str(directorycounter)  
        if os.path.exists(dir_name) and os.path.isdir(dir_name): 
            if not os.listdir(dir_name):  
                print("Skipping empty directory")
                skip = True  
                directorycounter += 1
            else:
                skip = False  
            
                htmlfile = open("wk" + str(directorycounter) + "/index.html", encoding="utf8")
                soup = BeautifulSoup(htmlfile, 'lxml')
                soup = soup.title
                title = '<h2>' + str(soup) + '</h2>'
                powerpoint = '<a href="https://mikhail-cct.github.io/ooapp/wk' + str(
                    directorycounter) + '/">' + '<img src="data:image/png;base64,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" width="50" /> <b><h3>Powerpoint</h3></b>' + '</a> '
                video = '<a href="' + "https://drive.google.com/file/d/"+NewLinks[directorycounter-1]+"/view?usp=sharing" + '"/><img src="https://upload.wikimedia.org/wikipedia/commons/6/68/Video_camera_icon.svg" ' \
                                                                        'width="50" /><b><h3>Recording</h3></b></a> '                                                    
                pdf = '<a href="https://github.com/mikhail-cct/ca3-test/raw/master/wk{}/wk{}.pdf"><img ' \
                        'src="https://banner2.cleanpng.com/20180802/ezo/kisspng-pdf-computer-file-clip-art-file-format-document-international-conference-on-materials-energy-april-5b630034a89c51.9879975015332147726906.jpg" width="50" ' \
                        '/><b><h3>PDF</h3></b></a>'.format(
                    str(directorycounter),
                    str(directorycounter))
                summary = title + '<hr> ' + video + '<hr> ' + powerpoint + '<hr> ' + pdf
                data = [{'type': 'num', 'section': 0, 'summary': '', 'summaryformat': 1, 'visible': 1, 'highlight': 0,
                            'sectionformatoptions': [{'name': 'level', 'value': '1'}]}]
                
                data[0]['summary'] = summary
            
                data[0]['section'] = directorycounter
            
                sec_write = LocalUpdateSections(courseid, data)
                if not skip:
                    print( "Sent section: "  + str(directorycounter))
                directorycounter += 1
        else:
            print("Issue some where")
            directorycounter += 1
except:
    print("Error in uploading")
FolderSystem()
print(FileSystem)