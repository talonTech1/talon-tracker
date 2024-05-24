from pymongo import MongoClient
from datetime import datetime
from time import sleep as wait
from flask import Flask, request, jsonify
cluster = MongoClient("mongodb+srv://smcs2026talontech:lUxhcscK1PDAhJxm@talontracker.k6uzv05.mongodb.net/?retryWrites=true&w=majority&appName=TalonTracker")
db = cluster["Tracker"]
locs = db["Locations"]

def removeLoc(locationN):
    locs.delete_one({"locN" : locationN.upper()})
def addLoc(locationN, fav = False):
    n = locationN.upper()
    d = datetime.now()

    if checkIfExisting(locationN):
        setToCurrentLoc(n)
        return False

    add = {"locN":n,"time":d,"count":1,"f":fav}
    locs.insert_one(add)
    return True
def getAllLocs():
    return [i for i in list(locs.find())]
def getFavorites():
    return [j for j in list(locs.find({"f":True}))]
def checkIfExisting(locationN):
    locationN = locationN.upper()
    check = locs.find_one({"locN":locationN})
    #print("check",check, check == None)
    return locs.find_one({"locN":locationN}) != None
def sortbyRecent():
    all = getAllLocs()
    return sorted(all, key = lambda x: x["time"], reverse=True)
def sortbyUsage():
    all = getAllLocs()
    return sorted(all, key = lambda x: x["count"], reverse=True)
def sortAlpha():
    all = getAllLocs()
    return sorted(all, key = lambda x: x['locN'])
def setToCurrentLoc(locationN):
    n = locationN.upper()
    currentCount = locs.find_one({"locN":n})["count"]
    locs.update_one({"locN": n}, {"$set": {"time": datetime.now()}})
    locs.update_one({"locN": n}, {"$set": {"count": currentCount + 1}})
def setFavorite(locationN,fav):
    n = locationN.upper()
    locs.update_one({"locN": n}, {"$set": {"f": fav}})
all = getAllLocs()
'''removeLoc("media center")
removeLoc("rm45")
addLoc("media center",True)
addLoc("office",True)
addLoc("smcs hub",False)
setToCurrentLoc("office")'''
for x in all:
    print("-------------------------")
    for j in list(x.items())[1:]: #no id
        print(j[0] + ": " + str(j[1]))
# API endpoints


cluster.close()
