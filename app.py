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
locations = db["LocationsCopy"]


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
    if n.isnumeric() and len(n) == 4:
        n = "ROOM " + n
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
    if request.headers.getlist("X-Forwarded-For"):
       ip = request.headers.getlist("X-Forwarded-For")[0]
    else:
       ip = request.remote_addr
    return ip


@app.route('/logout')
@login_required
def logout():
    session.pop('logged_in', None)
    flash('You were logged out.')
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)
    cluster.close()
