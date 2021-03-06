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
def list_Folders(dir):                                                                                                  
    r = []                                                                                                            
    subdirs = [x[0] for x in os.walk(dir)]                                                                            
    for subdir in subdirs:                                                                                            
        files = os.walk(subdir).__next__()[2]                                                                             
        r.append(os.path.join(subdir))                                                                        
    return r  
listOFContent = list_files("SEMONE")
folders = list_Folders("SEMONE")
#print(listOFContent)
print(folders)


# Module variables to connect to moodle api:
# Insert token and URL for your site here.
# Mind that the endpoint can start with "/moodle" depending on your installation.
KEY = "8cc87cf406775101c2df87b07b3a170d"
URL = "https://034f8a1dcb5c.eu.ngrok.io"
ENDPOINT = "/webservice/rest/server.php"


def rest_api_parameters(in_args, prefix='', out_dict=None):
    """Transform dictionary/array structure to a flat dictionary, with key names
    defining the structure.
    Example usage:
    >>> rest_api_parameters({'courses':[{'id':1,'name': 'course1'}]})
    {'courses[0][id]':1,
     'courses[0][name]':'course1'}
    """
    if out_dict == None:
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


def call(fname, **kwargs):
    """Calls moodle API function with function name fname and keyword arguments.
    Example:
    >>> call_mdl_function('core_course_update_courses',
                           courses = [{'id': 1, 'fullname': 'My favorite course'}])
    """
    parameters = rest_api_parameters(kwargs)
    parameters.update(
        {"wstoken": KEY, 'moodlewsrestformat': 'json', "wsfunction": fname})
    # print(parameters)
    response = post(URL+ENDPOINT, data=parameters).json()
    if type(response) == dict and response.get('exception'):
        raise SystemError("Error calling Moodle API\n", response)
    return response

################################################
# Rest-Api classes
################################################


class LocalGetSections(object):
    """Get settings of sections. Requires courseid. Optional you can specify sections via number or id."""

    def __init__(self, cid, secnums=[], secids=[]):
        self.getsections = call('local_wsmanagesections_get_sections',
                                courseid=cid, sectionnumbers=secnums, sectionids=secids)




class LocalUpdateSections(object):
    """Updates sectionnames. Requires: courseid and an array with sectionnumbers and sectionnames"""
    def __init__(self, cid, sectionsdata):
        self.updatesections = call('local_wsmanagesections_update_sections', courseid = cid, sections = sectionsdata)
        

################################################
# Example

courseid = "34"  # Exchange with valid id.
# Get all sections of the course.
sec = LocalGetSections(courseid)
# for i in sec:

#     print(json.dumps(i['summary'], indent=4, sort_keys=True))





data = [{'type': 'num', 'section': 3, 'summary': 'This oisin bitch ', 'summaryformat': 1, 'visible': 1 , 'highlight': 0, 'sectionformatoptions': [{'name': 'level', 'value': '1'}]}]

# Assemble the correct summary
summary = '<a href="https://mikhail-cct.github.io/ca3-test/wk1/slides.md">Week 10: this the slides </a><br>'+'<a href="https://mikhail-cct.github.io/ca3-test/wk1/wk1.pdf">Week 1: this is a pdg</a><br>'+'<a href="https://mikhail-cct.github.io/ca3-test/wk1/index.html"> this is the html file</a><br>'

# Assign the correct summary
data[0]['summary'] = summary

# Set the correct section number
data[0]['section'] = 10
Count = 1
summary = '<a href="https://mikhail-cct.github.io/ca3-test/wk1/slides.md">Week 10: this the slides </a><br>'+'<a href="https://mikhail-cct.github.io/ca3-test/wk1/wk1.pdf">Week 1: this is a pdg</a><br>'+'<a href="https://mikhail-cct.github.io/ca3-test/wk1/index.html"> this is the html file</a><br>'

# try:
# Write the data back to Moodle 
print(json.dumps(sec.getsections[1]["sectionnum"], indent=4, sort_keys=True))
for section in sec.getsections:
    num =data[0]['section']
    data[0]['summary'] = '<a href="https://mikhail-cct.github.io/ca3-test/wk'+ str(num) + '/slides.md">Week '+ str(num) + ': this the slides </a><br>'+'<a href="https://mikhail-cct.github.io/ca3-test/wk'+ str(num) + '/wk'+ str(num) + '.pdf">Week '+ str(num) + ': this is a pdf</a><br>'+'<a href="https://mikhail-cct.github.io/ca3-test/wk'+ str(num) + '/index.html"> week '+ str(num) + ': this is the html file</a><br>'
    data[0]['section'] = section['sectionnum']
    sec_write = LocalUpdateSections(courseid, data)
    if(data[0]['summary']==""):
        num =data[0]['section']
       
        print("blank section")
    elif(data[0]['summary']=="poo"):
        data[0]['summary'] = '<a href="https://mikhail-cct.github.io/ca3-test/wk'+ num + '/slides.md">Week '+ num + ': this the slides </a><br>'+'<a href="https://mikhail-cct.github.io/ca3-test/wk'+ num + '/wk'+ num + '.pdf">Week '+ num + ': this is a pdf</a><br>'+'<a href="https://mikhail-cct.github.io/ca3-test/wk'+ num + '/index.html"> week '+ num + ': this is the html file</a><br>'
        data[0]['section'] = section['sectionnum']
        sec_write = LocalUpdateSections(courseid, data)
# for section in LocalGetSections(sectionnum):
#     # Count =section['section']
#     print("issue?")
#     if(listOFContent)
#     # data[0]['summary'] = '<a href="https://mikhail-cct.github.io/ca3-test/wk1/slides.md">Week 10: this the slides </a><br>'+'<a href="https://mikhail-cct.github.io/ca3-test/wk1/wk1.pdf">Week 1: this is a pdg</a><br>'+'<a href="https://mikhail-cct.github.io/ca3-test/wk1/index.html"> this is the html file</a><br>'
#     # data[0]['section'] = section['section']
#     # sec_write = LocalUpdateSections(courseid, data)
print ("sent....")

# except:
print ("failed....")
