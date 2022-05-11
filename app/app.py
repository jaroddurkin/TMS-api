from flask import Flask
from flask import request
import requests
from datetime import datetime

from scraper.getter import getSectionsForClassAndTerm, getSectionDetailedForClassAndTerm

app = Flask(__name__)

@app.route("/health", methods=['GET'])
def health():
    res = {"health": "ok"}

    before = datetime.now()
    http = requests.get("https://termmasterschedule.drexel.edu")
    after = datetime.now()
    if http.status_code == 200:
        res["tms_health"] = "ok"
        time = after - before
        res["ping"] = time.microseconds // 1000
    else:
        res["tms_health"] = "error"

    return res

@app.route("/<string:term>/<string:code>")
def getAllClassesForTerm(term, code):
    objects = getSectionsForClassAndTerm(code, term)

    if request.args.get("method"):
        newobjs = []
        method = request.args.get("method").lower()
        query = ""
        if method == "f2f":
            query = "Face To Face"
        elif method == "hybrid":
            query = "Hybrid"
        elif method == "async":
            query = "Remote Asynchronous"
        elif method == "sync":
            query = "Remote Synchronous"
        elif method == "online":
            query = "Online"

        for section in objects:
            if section.method == query:
                newobjs.append(section)

        objects = newobjs

    if request.args.get("prof"):
        newobjs = []
        query = request.args.get("prof").lower()
        for section in objects:
            if query in section.prof.lower():
                newobjs.append(section)

        objects = newobjs
    
    if request.args.get("full"):
        newobjs = []
        query = request.args.get("full").lower()
        for section in objects:
            if str(section.full).lower() == query:
                newobjs.append(section)
        
        objects = newobjs


    res = {"sections": []}
    for section in objects:
        obj = {}
        obj["type"] = section.type
        obj["method"] = section.method
        obj["sec"] = section.sec
        obj["crn"] = section.crn
        obj["full"] = section.full
        obj["prof"] = section.prof
        obj["time"] = section.time
        res["sections"].append(obj)

    return res

@app.route("/<string:term>/<string:code>/details")
def getDetailedClassesForTerm(term, code):
    objects = getSectionDetailedForClassAndTerm(code, term)

    if request.args.get("method"):
        newobjs = []
        method = request.args.get("method").lower()
        query = ""
        if method == "f2f":
            query = "Face To Face"
        elif method == "hybrid":
            query = "Hybrid"
        elif method == "async":
            query = "Remote Asynchronous"
        elif method == "sync":
            query = "Remote Synchronous"
        elif method == "online":
            query = "Online"

        for section in objects:
            if section.method == query:
                newobjs.append(section)

        objects = newobjs

    if request.args.get("prof"):
        newobjs = []
        query = request.args.get("prof").lower()
        for section in objects:
            if query in section.prof.lower():
                newobjs.append(section)

        objects = newobjs


    res = {"sections": []}
    for section in objects:
        obj = {}
        obj["type"] = section.type
        obj["method"] = section.method
        obj["sec"] = section.sec
        obj["crn"] = section.crn
        obj["full"] = section.full
        obj["prof"] = section.prof
        obj["time"] = section.time
        obj["cred"] = section.credits
        obj["campus"] = section.campus
        obj["seats"] = section.seats
        obj["enroll"] = section.enroll
        obj["avail"] = section.available
        obj["text"] = section.comments
        obj["build"] = section.building
        obj["room"] = section.room
        res["sections"].append(obj)

    return res
