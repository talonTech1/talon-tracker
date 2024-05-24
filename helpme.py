from pymongo import MongoClient
cluster = MongoClient ("mongodb+srv://smcs2026talontech:lUxhcscK1PDAhJxm@talontracker.k6uzv05.mongodb.net/?retryWrites=true&w=majority&appName=TalonTracker")
db = cluster["Tracker"]
fav = db["Favorites"]

post = {"name:" : "bobby", "score" : 12}

fav.insert_one(post)