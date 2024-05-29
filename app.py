from flask import Flask,render_template,request
app = Flask(__name__)
from pymongo import MongoClient
from datetime import datetime
from time import sleep
cluster = MongoClient("mongodb+srv://smcs2026talontech:lUxhcscK1PDAhJxm@talontracker.k6uzv05.mongodb.net/?retryWrites=true&w=majority&appName=TalonTracker")
db = cluster["Tracker"]
locations = db["Locations"]
f1 = False
r1 = False
u1 = False
#chrome://net-internals/#sockets

def removeLoc(locationN):
    locations.delete_one({"locN" : locationN.upper()})
def addLoc(locationN, fav = False):
    n = locationN.upper()
    d = datetime.now()

    if checkIfExisting(locationN):
        setToCurrentLoc(n)
        return False

    add = {"locN":n,"time":d,"count":1,"f":fav,"current" : True}
    locations.insert_one(add)
    return True
def checkIfExisting(locationN):
    return locations.find_one({"locN":locationN.upper()}) != None
def removeCurrent(locationN):
    locations.update_one({"locN": locationN.upper()}, {"$set": {"current": False}})
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
def sortbyUsage(li):
    # return (list(locations.find().sort("count")))
    return sorted(li, key = lambda x: x["count"], reverse=True)
def sortbyRecent(li):
    # return (list(locations.find().sort("time")))
    return sorted(li, key = lambda x: x["time"])
@app.route("/", methods= ["POST","GET"])
def index():
    global f1
    global r1
    global u1
    sleep(0.2)
    if request.method == "POST":
        try:
            if request.form['addLoc']:
                return render_template('add.html')
        except KeyError:
            pass
        try:
            if request.form['locate']:
                addLoc(request.form['locate'])
        except KeyError:
            pass
        try:
            if request.form['setCurrent']:
                if request.form['setCurrent'][-1] == "F":
                    removeCurrent(request.form['setCurrent'][:-1])
                else:
                    setToCurrentLoc(request.form['setCurrent'][:-1])
        except KeyError:
            pass
        try:
            if request.form['remove']:
                removeLoc(request.form['remove'])
        except KeyError:
            pass
        try:
            if request.form['setFav']:
                if request.form['setFav'][-1] == "T":
                    setFavorite(request.form['setFav'][:-1],True)
                else:
                    setFavorite(request.form['setFav'][:-1], False)
        except KeyError:
            pass
        try:
            if request.form["showFavs"]:
                if request.form["showFavs"] == "T":
                    f1 = True
                    r1 = False
                    u1 = False
                else:
                    f1 = False
        except:
            pass
        try:
            if request.form["showRecents"]:
                if request.form["showRecents"] == "T":
                    r1 = True
                    f1 = False
                    u1 = False
                else:
                    r1 = False
        except:
            pass
    if f1:
        return render_template('index.html', fav=f1, use=False, recent=r1, locs=reversed(list(locations.find({"f": True}))),
                               current=locations.find_one({"current": True}))

    elif r1:
        return render_template('index.html', fav=f1, use=False, recent=r1, locs=sortbyRecent(list(locations.find())),
                               current=locations.find_one({"current": True}))

    return render_template('index.html',fav=f1,use=False,recent=r1, locs=reversed(list(locations.find())),current=locations.find_one({"current" : True}))

if __name__ == "__main__":
    app.run(debug=True)
    cluster.close()

'''
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
'''