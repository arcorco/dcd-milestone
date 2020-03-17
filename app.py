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
def get_games():
    return render_template('games.html', games=mongo.db.games.find())
    
@app.route('/add_game')
def add_game():
    return render_template('addgame.html')

@app.route('/insert_game', methods=['POST'])
def insert_game():
    games = mongo.db.games
    new_game = request.form.to_dict()
    min_players = new_game.get("number_of_players_min")
    max_players = new_game.get("number_of_players_max")
    min_age = new_game.get("age_range")
    age = "%s+" % min_age
    players = "%s-%s" % (min_players, max_players)
    new_game.update( {'number_of_players' : players} )
    new_game.update( {'age_range' : age} )
    new_game.pop('number_of_players_min')
    new_game.pop('number_of_players_max')
    
    games.insert_one(new_game)
    return redirect(url_for('get_games'))

if __name__ == "__main__":
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)