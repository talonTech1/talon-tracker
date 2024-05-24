from pymongo import MongoClient
from datetime import datetime
cluster = MongoClient("mongodb+srv://smcs2026talontech:lUxhcscK1PDAhJxm@talontracker.k6uzv05.mongodb.net/?retryWrites=true&w=majority&appName=TalonTracker")
db = cluster["Tracker"]
locs = db["Locations"]

def removeLoc(locationN):
    locs.delete_one({"locN" : locationN.upper()})
def addLoc(locationN, fav = False):
    n = locationN.upper()
    d = datetime.timestamp(datetime.now())

    if checkIfExisting(locationN):
        currentCount = locs.find_one({"locN":n})["count"]
        locs.update_one({"locN":n}, {"$set":{"count":currentCount + 1}})
        locs.update_one({"locN": n}, {"$set": {"time":d}})
        return False

    add = {"locN":n,"time":d,"count":0,"f":fav}
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
def sortByRecent():
    all = getAllLocs()
    return sorted(all, key=lambda x: x["time"])
def sortbyUsage():
    all = getAllLocs()
    return sorted(all, key=lambda x: x["usage"])
def sortAlpha():
    all = getAllLocs()
    sorted(all, key=lambda x: x['locN'])
if input() == "a":
    addLoc(input(),True)
print(getAllLocs())
print(getFavorites())
print(sortByRecent())
print(checkIfExisting("rm23321"))
cluster.close()
