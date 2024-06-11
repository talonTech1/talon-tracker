from flask import Flask,render_template,request,url_for,request,redirect,flash,session
app = Flask(__name__)
from pymongo import MongoClient
from datetime import datetime
from time import sleep
from functools import wraps
from calendar import monthrange
app.secret_key = 'my precious'

# login required decorator
cluster = MongoClient("mongodb+srv://smcs2026talontech:lUxhcscK1PDAhJxm@talontracker.k6uzv05.mongodb.net/?retryWrites=true&w=majority&appName=TalonTracker")
db = cluster["Tracker"]
locations = db["Locations"]


f1 = False
r1 = False
u1 = False
s1 = False
#chrome://net-internals/#sockets
def convertUTC(dt):
    # datetime(year, month, day, hour, minute, second, microsecond)
    newH = dt.hour - 4
    y,m,d,minute = dt.year,dt.month,dt.day,dt.minute
    if newH < 0:
        newH = 24 + newH
        if dt.day < 0:
            if dt.month < 0:
                m = 12
                y -= 1
            d = monthrange(y,m)
        else:
            d -= 1

    return datetime(y,m,d,newH,minute)
def removeLoc(locationN):
    locations.delete_one({"locN" : locationN.upper()})
def checkIfExisting(locationN):
    return locations.find_one({"locN":locationN.upper()}) != None
def removeCurrent(locationN):
    locations.update_one({"locN": locationN.upper()}, {"$set": {"current": False}})
def setToCurrentLoc(locationN):
    n = locationN.upper()
    d = convertUTC(datetime.utcnow())

    currentCount = locations.find_one({"locN":n})["count"]
    locations.update_one({"locN": n}, {"$set": {"time": d}})
    locations.update_one({"locN": n}, {"$set": {"count": currentCount + 1}})
    locations.update_one({"current": True}, {"$set": {"current": False}})
    locations.update_one({"locN": n}, {"$set": {"current": True}})

def addLoc(locationN, fav = False):
    n = locationN.upper()
    d = convertUTC(datetime.utcnow())
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
    return sorted(li, key = lambda x: x["time"],reverse=True)

def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('login'))
    return wrap



@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['password'] != 'blair':
            error = 'Invalid. Try Again.'
        else:
            session['logged_in'] = True
            flash('You were logged in.')
            return redirect('/')
    return render_template('login.html', error=error)

@app.route("/", methods= ["POST","GET"])
@login_required
def index():
    global f1
    global r1
    global u1
    global s1
    sleep(0.15)
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
        try:
            if request.form["showUsage"]:
                if request.form["showUsage"] == "T":
                    r1 = False
                    f1 = False
                    u1 = True
                else:
                    u1 = False
        except:
            pass
        try:
            if request.form["viewLoc"]:
                if request.form["viewLoc"] == "T":
                    s1 = True
                else:
                    s1 = False
        except:
            pass
    if not s1:
        return render_template('index.html', show=s1, fav=f1, use=u1, recent=r1,
                               locs=[],
                               current=locations.find_one({"current": True}))
    elif f1:
        return render_template('index.html',show= s1, fav=f1, use=u1, recent=r1, locs=reversed(list(locations.find({"f": True}))),
                               current=locations.find_one({"current": True}))

    elif r1:
        return render_template('index.html',show =s1, fav=f1, use=u1, recent=r1, locs=sortbyRecent(list(locations.find())),
                               current=locations.find_one({"current": True}))
    elif u1:
        return render_template('index.html',show=s1,  fav=f1, use=u1, recent=r1, locs=sortbyUsage(list(locations.find())),
                               current=locations.find_one({"current": True}))
    return render_template('index.html', show=s1, fav=f1,use=u1,recent=r1, locs=reversed(list(locations.find())),current=locations.find_one({"current" : True}))


@app.route('/logout')
@login_required
def logout():
    session.pop('logged_in', None)
    flash('You were logged out.')
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)
    cluster.close()
