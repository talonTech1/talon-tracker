from pymongo import MongoClient
from datetime import datetime
from flask import Flask
from flask_pymongo import PyMongo
cluster = MongoClient("mongodb+srv://smcs2026talontech:lUxhcscK1PDAhJxm@talontracker.k6uzv05.mongodb.net/?retryWrites=true&w=majority&appName=TalonTracker")
db = cluster["Tracker"]
locations = db["Locations"]

def removeLoc(locationN):
    locations.delete_one({"locN" : locationN.upper()})
def getAllLocs():
    return [i for i in list(locations.find())]
def getFavorites():
    return [j for j in list(locations.find({"f":True}))]
def checkIfExisting(locationN):
    return locations.find_one({"locN":locationN.upper()}) != None
def sortbyRecent(li):
    # return (list(locations.find().sort("time")))
    return sorted(li, key = lambda x: x["time"], reverse=True) #this somehow works for datetime objects :D
def sortbyUsage(li):
    # return (list(locations.find().sort("count")))
    return sorted(li, key = lambda x: x["count"], reverse=True)
def sortAlpha(li):
    # return (list(locations.find().sort("locN")))
    return sorted(li, key = lambda x: x['locN'])
def setToCurrentLoc(locationN):
    n = locationN.upper()
    currentCount = locations.find_one({"locN":n})["count"]
    locations.update_one({"locN": n}, {"$set": {"time": datetime.now()}})
    locations.update_one({"locN": n}, {"$set": {"count": currentCount + 1}})
    locations.update_one({"current": True}, {"$set": {"current": False}})
    locations.update_one({"locN": n}, {"$set": {"current": True}})
def addLoc(locationN, fav = False):
    n = locationN.upper()
    d = datetime.now()

    if checkIfExisting(locationN):
        setToCurrentLoc(n)
        return False
    try:
        locations.update_one({"current": True}, {"$set": {"current": False}})
    except:
        pass
    add = {"locN":n,"time":d,"count":1,"f":fav,"current":True}
    locations.insert_one(add)
    return True
def setFavorite(locationN,fav):
    n = locationN.upper()
    locations.update_one({"locN": n}, {"$set": {"f": fav}})
addLoc("media center")
addLoc("rm345")
addLoc("smcs hub")
addLoc("out")
# just to print and see whats up yk?


cluster.close()
