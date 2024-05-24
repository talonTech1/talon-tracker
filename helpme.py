from pymongo import MongoClient
from datetime import datetime
cluster = MongoClient ("mongodb+srv://smcs2026talontech:lUxhcscK1PDAhJxm@talontracker.k6uzv05.mongodb.net/?retryWrites=true&w=majority&appName=TalonTracker")
db = cluster["Tracker"]
locs = db["Locations"]
def addLoc(locationN, fav = False):
    if checkIfExisting:
        return False
    n = locationN.upper()
    d = datetime.timestamp(datetime.now())
    add = {"locN":n, "time":d, "f":fav}
    locs.insert_one(add)
    return True
def getAllLocs():
    return [i for i in list(locs.find())]
def checkIfExisting(locationN):
    locationN = locationN.upper()
    check = locs.find_one({"locN":locationN})
    return locs.find_one({"locN":locationN}) != None

if input() == "a":
    addLoc("rm23321")
    addLoc("media center")
print(getAllLocs())
print(checkIfExisting("rm23321"))
cluster.close()
