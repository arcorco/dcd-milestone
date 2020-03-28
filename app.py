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
    games.insert_one(new_game)
    return redirect(url_for('get_games'))
    
@app.route('/edit_game/<game_id>')
def edit_game(game_id):
    the_game = mongo.db.games.find_one({"_id": ObjectId(game_id)})
    return render_template('editgame.html', game=the_game)

@app.route('/update_game/<game_id>', methods=["POST"])
def update_game(game_id):
    games = mongo.db.games
    games.update( {'_id': ObjectId(game_id)},
    {   
        'game_name':request.form.get('game_name'),
        'game_description':request.form.get('game_description'),
        'manufacturer':request.form.get('manufacturer'),
        'number_of_players_min':request.form.get('number_of_players_min'),
        'number_of_players_max':request.form.get('number_of_players_max'),
        'number_of_players':"%s-%s" % (request.form.get('number_of_players_min'), request.form.get('number_of_players_max')),
        'age_range': "%s+" % (request.form.get('age_range'))
    })
    return redirect(url_for('get_games'))

@app.route('/delete_game/<game_id>')
def delete_game(game_id):
    mongo.db.games.remove({'_id': ObjectId(game_id)})
    return redirect(url_for('get_games'))
    
@app.route('/get_reviews')
def get_reviews():
    return render_template('reviews.html', reviews=mongo.db.reviews.find())
    
@app.route('/add_review')
def add_review():
    return render_template('addreview.html', games=mongo.db.games.find())
    
@app.route('/insert_review', methods=['POST'])
def insert_review():
    reviews = mongo.db.reviews
    new_review = request.form.to_dict()
    recommended = new_review.get("recommended")
    if recommended == "on":
        new_review.update( {'recommended' : 'Yes'} )
    else:
        new_review.update( {'recommended' : 'No' })
    reviews.insert_one(new_review)
    return redirect(url_for('get_reviews'))
    
@app.route('/edit_review/<review_id>')
def edit_review(review_id):
    the_review = mongo.db.reviews.find_one({"_id": ObjectId(review_id)})
    return render_template('editreview.html', review=the_review, games=mongo.db.games.find())
    
@app.route('/update_review/<review_id>', methods=["POST"])
def update_review(review_id):
    reviews = mongo.db.reviews
    updated_review = request.form.to_dict()
    recommended = updated_review.get("recommended")
    if recommended == "on":
        reviews.update({'_id':ObjectId(review_id)},
        {
            'game_name':request.form.get('game_name'),
            'review':request.form.get('review'),
            'rating':request.form.get('rating'),
            'recommended': "Yes"
        })
    else:
        reviews.update({'_id':ObjectId(review_id)},
        {
            'game_name':request.form.get('game_name'),
            'review':request.form.get('review'),
            'rating':request.form.get('rating'),
            'recommended': "No"
        })
    return redirect(url_for('get_reviews'))

@app.route('/delete_review/<review_id>')
def delete_review(review_id):
    mongo.db.reviews.remove({'_id': ObjectId(review_id)})
    return redirect(url_for('get_reviews'))

if __name__ == "__main__":
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)