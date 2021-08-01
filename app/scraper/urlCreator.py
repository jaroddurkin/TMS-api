import requests
from bs4 import BeautifulSoup
import json

PAGE = "https://termmasterschedule.drexel.edu"

def getTermLink(term):
    res = requests.get(PAGE + "/webtms_du/app")
    content = BeautifulSoup(res.content, "html.parser")

    terms = content.find_all("div", {"class": "term"})
    for entry in terms:
        text = entry.text.split()
        if text[0][:2].lower() == term[:2].lower() and text[2][:2] == term[2:]:
            return entry.a["href"]
    return None

def findCollegeLink(abbrev, term):
    termlink = getTermLink(term)
    if not termlink:
        return None

    res = requests.get(PAGE + termlink)
    content = BeautifulSoup(res.content, "html.parser")

    letters = ""
    for i in abbrev:
        if i.isalpha():
            letters += i
    college = ""
    with open("./static/collegemaps.json") as file:
        data = json.load(file)
        college += data[letters]

    colist = content.find_all("div", {"id": "sideLeft"})
    for entry in colist:
        alist = entry.find_all("a")
        for a in alist:
            if a.text == college:
                return a["href"]

    return None

def findClassLink(abbrev, term):

    collegelink = findCollegeLink(abbrev, term)
    if not collegelink:
        return None

    letters = ""
    for i in abbrev:
        if i.isalpha():
            letters += i

    res = requests.get(PAGE + collegelink)
    content = BeautifulSoup(res.content, "html.parser")

    classes = content.find_all("div", {"class": ["odd", "even"]})

    for entry in classes:
        alist = entry.find_all("a")
        for a in alist:
            parencnt = 0
            cabbrev = ""
            for i in a.text:
                if parencnt > 1:
                    break
                if i == "(" or i == ")":
                    parencnt += 1
                    continue
                if parencnt == 1:
                    cabbrev += i
            if cabbrev == letters:
                return PAGE + a["href"]

    return None
