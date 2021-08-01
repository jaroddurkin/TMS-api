import requests
from bs4 import BeautifulSoup
from scraper.urlCreator import findClassLink

class Section:

    def __init__(self, abbrev, type, method, sec, crn, prof, time):
        self.abbrev = abbrev
        self.type = type
        self.method = method
        self.sec = sec
        self.crn = crn
        self.prof = prof
        self.time = time

    def __str__(self):
        outputstr = ""
        outputstr += self.abbrev + " | "
        outputstr += self.type + " | "
        outputstr += self.method + " | "
        outputstr += self.sec + " | "
        outputstr += self.crn + " | "
        outputstr += self.time + " | "
        outputstr += self.prof
        return outputstr

def createClassList(abbrev, term):
    classlink = findClassLink(abbrev, term)
    if not classlink:
        return None

    res = requests.get(classlink)
    content = BeautifulSoup(res.content, "html.parser")
    classes = content.find_all("tr", {"class": ["even", "odd"]})

    letters = ""
    for i in abbrev:
        if i.isalpha():
            letters += i

    numbers = ""
    for i in abbrev:
        if i.isdigit():
            numbers += i

    classlist = []
    for entry in classes:
        tdlist = entry.find_all("td")
        if tdlist[0].text != letters:
            continue
        for i in tdlist:
            if i.text == numbers:
                classlist.append(entry)

    return classlist

def makeObjects(classlist):

    objs = []
    if not classlist:
        return objs

    for i in classlist:
        colnum = 0
        collist = i.find_all("td", {"valign": ["top", "center"]})
        collist += i.find_all("td", {"colspan": 2})
        struct = []
        for j in collist:
            if colnum == 1:
                struct[0] += j.text
            elif colnum == 5:
                alist = j.find_all("a")
                for a in alist:
                    struct.append(a.text)
            elif colnum == 6:
                colnum += 1
                continue
            elif colnum == 8:
                struct.append("")
                tdlist = j.find_all("td", {"align": "center"})
                struct[6] += tdlist[0].text + " "
                struct[6] += tdlist[1].text
            else:
                struct.append(j.text)
            colnum += 1

        classobj = Section(struct[0], struct[1], struct[2], struct[3], struct[4], struct[5], struct[6])
        objs.append(classobj)
    return objs
