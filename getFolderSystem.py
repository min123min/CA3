from requests import get, post
import json
from dateutil import parser
import datetime
import requests
import lxml
import bs4
import os
import codecs

fileCollection = []
subfolderCollection = []
num1 = 0
def list_files(dir):                                                                                                  
    r = []                                                                                                            
    subdirs = [x[0] for x in os.walk(dir)]                                                                            
    for subdir in subdirs:                                                                                            
        files = os.walk(subdir).__next__()[2]                                                                             
        if (len(files) > 0):                                                                                          
            for file in files:                                                                                        
                r.append(os.path.join(subdir, file))                                                                         
    return r     
print(list_files("SEM1"))
f = open('SEM1/wk1/index.html','w+')
print(f)
44


f=codecs.open("SEM1/wk2/index.html", 'r')
print (f.read())