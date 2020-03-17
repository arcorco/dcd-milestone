import os
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

app = Flask(__name__)

app.config["MONGO_DNAME"] = 'game_review'
app.config["MONGO_URI"] = 'mongodb+srv://first_user:WG9zKqgDwfDTHNa@myfirstcluster-74ub4.mongodb.net/game_review?retryWrites=true&w=majority'
#environment variable for username and password

mongo = PyMongo(app)

@app.route('/')
@app.route('/get_games')
def get_tasks():
    return render_template("games.html", games=mongo.db.games.find())
    
@app.route('/add_game')
def add_game():
    return render_template("addgame.html")

if __name__ == "__main__":
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)