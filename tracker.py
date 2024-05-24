from pymongo import MongoClient
from datetime import datetime
from time import sleep as wait
from flask import Flask, request, jsonify
cluster = MongoClient("mongodb+srv://smcs2026talontech:lUxhcscK1PDAhJxm@talontracker.k6uzv05.mongodb.net/?retryWrites=true&w=majority&appName=TalonTracker")
db = cluster["Tracker"]
locations = db["Locations"]

def removeLoc(locationN):
    locations.delete_one({"locN" : locationN.upper()})
def addLoc(locationN, fav = False):
    n = locationN.upper()
    d = datetime.now()

    if checkIfExisting(locationN):
        setToCurrentLoc(n)
        return False

    add = {"locN":n,"time":d,"count":1,"f":fav}
    locations.insert_one(add)
    return True
def getAllLocs():
    return [i for i in list(locations.find())]
def getFavorites():
    return [j for j in list(locations.find({"f":True}))]
def checkIfExisting(locationN):
    locationN = locationN.upper()
    check = locations.find_one({"locN":locationN})
    #print("check",check, check == None)
    return locations.find_one({"locN":locationN}) != None
def sortbyRecent(li):
    return sorted(li, key = lambda x: x["time"], reverse=True) #this somehow works for datetime objects :D
def sortbyUsage(li):
    return sorted(li, key = lambda x: x["count"], reverse=True)
def sortAlpha(li):
    return sorted(li, key = lambda x: x['locN'])
def setToCurrentLoc(locationN):
    n = locationN.upper()
    currentCount = locations.find_one({"locN":n})["count"]
    locations.update_one({"locN": n}, {"$set": {"time": datetime.now()}})
    locations.update_one({"locN": n}, {"$set": {"count": currentCount + 1}})
def setFavorite(locationN,fav):
    n = locationN.upper()
    locations.update_one({"locN": n}, {"$set": {"f": fav}})
all = getAllLocs()
for x in sortbyRecent(all):
    print("-------------------------")
    for j in list(x.items())[1:]: #no id
        print(j[0] + ": " + str(j[1]))
# API endpoints


cluster.close()
