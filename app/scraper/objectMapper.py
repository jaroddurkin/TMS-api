import requests
from bs4 import BeautifulSoup
from scraper.urlCreator import findClassLink

class Section:

    def __init__(self, abbrev, type, method, sec, crn, full, prof, time):
        self.abbrev = abbrev
        self.type = type
        self.method = method
        self.sec = sec
        self.crn = crn
        self.full = full
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
    
    def setDetails(self, details):
        self.credits = details["credits"]
        self.campus = details["campus"]
        self.seats = details["seats"]
        self.enroll = details["enroll"]
        self.available = details["available"]
        self.comments = details["comments"]
        self.building = details["building"]
        self.room = details["room"]


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

def makeObjects(classlist, isDetailed):

    objs = []
    if not classlist:
        return objs

    for i in classlist:
        colnum = 0
        collist = i.find_all("td", {"valign": ["top", "center"]})
        collist += i.find_all("td", {"colspan": 2})
        struct = []
        details = None
        for j in collist:
            if colnum == 1:
                struct[0] += j.text
            elif colnum == 5:
                alist = j.find_all("a")
                for a in alist:
                    struct.append(a.text)
                    if isDetailed:
                        details = a["href"]
                    if a.parent['title'] == "FULL":
                        struct.append(True)
                    else:
                        struct.append(False)
            elif colnum == 6:
                colnum += 1
                continue
            elif colnum == 8:
                struct.append("")
                tdlist = j.find_all("td", {"align": "center"})
                struct[7] += tdlist[0].text + " "
                struct[7] += tdlist[1].text
            else:
                struct.append(j.text)
            colnum += 1

        classobj = Section(struct[0], struct[1], struct[2], struct[3], struct[4], struct[5], struct[6], struct[7])
        classobj.setDetails(getDetailPage(details))
        objs.append(classobj)
    return objs

def getDetailPage(link):
    obj = {};
    res = requests.get("https://termmasterschedule.drexel.edu" + link)
    content = BeautifulSoup(res.content, "html.parser")
    info = content.find_all("td", {"class": ["even", "odd"]})
    # cred: 4, camp: 6, seats: 10, enroll: 11, "comments": 12
    if len(info) > 12:
        obj["credits"] = info[4].text.strip()
        obj["campus"] = info[6].text
        obj["seats"] = int(info[10].text)
        enroll = info[11].text
        if enroll == "CLOSED":
            obj["enroll"] = obj["seats"]
        else:
            obj["enroll"] = int(enroll)
        obj["available"] = obj["seats"] - obj["enroll"]
        obj["comments"] = info[12].text.replace("\n", "")


    extra = content.find_all("tr", {"class": "even"})
    extrainfo = extra[0].find_all("td")
    if len(extrainfo) > 5:
        obj["building"] = extrainfo[4].text
        obj["room"] = extrainfo[5].text
    
    return obj
    # building: 4, room: 5