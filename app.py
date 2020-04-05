import os
import statistics
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from os import path
if path.exists("env.py"):
  import env

app = Flask(__name__)

app.config["MONGO_DBNAME"] = 'game_review'
MONGO_URI = os.environ.get('MONGO_URI')
app.config["MONGO_URI"] = MONGO_URI
#environment variable for username and password

mongo = PyMongo(app)

@app.route('/')
@app.route('/home')
def home():
    return render_template('homepage.html', games=mongo.db.games.find())
  
#Sends images to MongoDB database (Credit: Pretty Printed on YouTube - https://www.youtube.com/watch?v=DsgAuceHha4 )  
@app.route('/file/<filename>')
def file(filename):
    return mongo.send_file(filename)

@app.route('/get_games')
def get_games():
    return render_template('games.html', games=mongo.db.games.find())

#Sort games database into alphabetical order
@app.route('/get_games/alphabetical')    
def sort_alpha():
    return render_template('games.html', games=mongo.db.games.aggregate([{"$sort" : {"game_name" : 1 }}]))

#Sort games database into most recently added    
@app.route('/get_games/most_recent')
def sort_recent():
    return render_template('games.html', games=mongo.db.games.aggregate([{"$sort" : {"_id" : -1 }}]))
 
#Sort games database into highest rated order    
@app.route('/get_games/highest_rated')
def sort_rated():
    return render_template('games.html', games=mongo.db.games.aggregate([{"$sort" : {"avg_rating" : -1 }}]))

#Filter games database into ratings of at least 2    
@app.route('/get_games/avg_rating2')
def avg_rating2():
    return render_template('games.html', games=mongo.db.games.find({"avg_rating" : {"$gt" : 1.9 }}))

#Filter games database into ratings of at least 3    
@app.route('/get_games/avg_rating3')
def avg_rating3():
    return render_template('games.html', games=mongo.db.games.find({"avg_rating" : {"$gt" : 2.9 }}))

#Filter games database into ratings of at least 4    
@app.route('/get_games/avg_rating4')
def avg_rating4():
    return render_template('games.html', games=mongo.db.games.find({"avg_rating" : {"$gt" : 3.9 }}))

#Filter games database into ratings of at least 5    
@app.route('/get_games/avg_rating5')
def avg_rating5():
    return render_template('games.html', games=mongo.db.games.find({"avg_rating" : {"$gt" : 4.9 }}))
    
@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')
    
@app.route('/add_game')
def add_game():
    return render_template('addgame.html')

#Takes form from addgame.html and creates a document in the games collection
@app.route('/insert_game', methods=['POST'])
def insert_game():
    if 'game_image' in request.files:
        game_image = request.files['game_image']
        mongo.save_file(game_image.filename, game_image)
    games = mongo.db.games
    new_game = request.form.to_dict()
    min_players = new_game.get("number_of_players_min")
    max_players = new_game.get("number_of_players_max")
    players = "%s-%s" % (min_players, max_players)
    new_game.update( {'number_of_players' : players} )
    new_game.update( {'game_image_name' : game_image.filename})
    games.insert_one(new_game)
    return redirect(url_for('get_games'))
    
@app.route('/edit_game/<game_id>')
def edit_game(game_id):
    the_game = mongo.db.games.find_one({"_id": ObjectId(game_id)})
    return render_template('editgame.html', game=the_game)

#Takes form from editgame.html and updates a document in the games collection
@app.route('/update_game/<game_id>', methods=["POST"])
def update_game(game_id):
    if 'game_image' in request.files:
        game_image = request.files['game_image']
        mongo.save_file(game_image.filename, game_image)
    games = mongo.db.games
    the_game = mongo.db.games.find_one({"_id": ObjectId(game_id)})
    game_image_name = the_game.get('game_image_name')
    if game_image_name == "":
        games.update( {'_id': ObjectId(game_id)},
        { '$set': { 
            'game_name':request.form.get('game_name'),
            'game_description':request.form.get('game_description'),
            'manufacturer':request.form.get('manufacturer'),
            'number_of_players_min':request.form.get('number_of_players_min'),
            'number_of_players_max':request.form.get('number_of_players_max'),
            'number_of_players':"%s-%s" % (request.form.get('number_of_players_min'), request.form.get('number_of_players_max')),
            'age_range': request.form.get('age_range'),
            'game_image_name': game_image.filename
        }})
    else:
        games.update_one( {'_id': ObjectId(game_id)},
        { '$set': { 
            'game_name':request.form.get('game_name'),
            'game_description':request.form.get('game_description'),
            'manufacturer':request.form.get('manufacturer'),
            'number_of_players_min':request.form.get('number_of_players_min'),
            'number_of_players_max':request.form.get('number_of_players_max'),
            'number_of_players':"%s-%s" % (request.form.get('number_of_players_min'), request.form.get('number_of_players_max')),
            'age_range': request.form.get('age_range')
        }})
    return redirect(url_for('get_games'))

#Deletes a chosen document in the games collection
@app.route('/delete_game/<game_id>')
def delete_game(game_id):
    mongo.db.games.remove({'_id': ObjectId(game_id)})
    return redirect(url_for('get_games'))
    
@app.route('/add_review')
def add_review():
    return render_template('addreview.html', games=mongo.db.games.find())
 
#Takes form from addreview.html and creates a document in the reviews collection    
@app.route('/insert_review', methods=['POST'])
def insert_review():
    games = mongo.db.games
    reviews = mongo.db.reviews
    new_review = request.form.to_dict()
    recommended = new_review.get("recommended")
    if recommended == "on":
        new_review.update( {'recommended' : 'Yes'} )
    else:
        new_review.update( {'recommended' : 'No' })
    reviews.insert_one(new_review)
    ratings = []
    for review in reviews.find():
        if review["game_name"] == new_review.get("game_name"):
            ratings.append(int(review['rating']))
    avg_rating = round(statistics.mean(ratings), 1)
    games.update({"game_name": new_review.get("game_name")},
    {"$set": {"avg_rating": avg_rating}})
    return redirect(url_for('get_games'))
    
@app.route('/edit_review/<review_id>')
def edit_review(review_id):
    the_review = mongo.db.reviews.find_one({"_id": ObjectId(review_id)})
    return render_template('editreview.html', review=the_review, games=mongo.db.games.find())
 
#Takes form from editreview.html and updates a document in the reviews collection      
@app.route('/update_review/<review_id>', methods=["POST"])
def update_review(review_id):
    games = mongo.db.games
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
    ratings = []
    for review in reviews.find():
        if review['game_name'] == updated_review.get("game_name"):
            ratings.append(int(review['rating']))
    avg_rating = round(statistics.mean(ratings), 1)
    games.update({"game_name": updated_review.get("game_name")},
    {"$set": {"avg_rating": avg_rating}})
    return redirect(url_for('get_games'))

#Deletes a chosen document in the reviews collection
@app.route('/delete_review/<review_id>')
def delete_review(review_id):
    deleted_review = mongo.db.reviews.find_one({'_id': ObjectId(review_id)})
    mongo.db.reviews.remove({'_id': ObjectId(review_id)})
    return redirect(url_for('get_games'))
 
#Read a selected game in the games database and display its information and the reviews from the reviews database of that particular game 
@app.route('/game_review/<game_name>')
def game_review(game_name):
    return render_template('gamereviews.html', reviews=mongo.db.reviews.find({"game_name": game_name}), game=mongo.db.games.find_one({"game_name": game_name}))

#Sort reviews database into most recently added and filters to show reviews with matching "game_name"
@app.route('/game_review/<game_name>/most_recent')
def recent_review(game_name):
    return render_template('gamereviews.html', reviews=mongo.db.reviews.aggregate([{"$sort" : {"_id" : -1 }}, {"$match" : { "game_name" : game_name }}]), game=mongo.db.games.find_one({"game_name": game_name}))

#Sort reviews database into highest rated order and filters to show reviews with matching "game_name"
@app.route('/game_review/<game_name>/highest_review')
def highest_review(game_name):
    return render_template('gamereviews.html', reviews=mongo.db.reviews.aggregate([{"$sort" : {"rating" : -1 }}, {"$match" : { "game_name" : game_name }}]), game=mongo.db.games.find_one({"game_name": game_name}))

#Sort reviews database into lowest rated order and filters to show reviews with matching "game_name"
@app.route('/game_review/<game_name>/lowest_review')
def lowest_review(game_name):
    return render_template('gamereviews.html', reviews=mongo.db.reviews.aggregate([{"$sort" : {"rating" : 1 }}, {"$match" : { "game_name" : game_name }}]), game=mongo.db.games.find_one({"game_name": game_name}))

#The following 5 app routes filter reviews database by "game_name" and "rating"
@app.route('/game_review/<game_name>/rating1')
def rating1(game_name):
    return render_template('gamereviews.html', reviews=mongo.db.reviews.find({"game_name" : game_name, "rating" : "1"}), game=mongo.db.games.find_one({"game_name": game_name}))

@app.route('/game_review/<game_name>/rating2')
def rating2(game_name):
    return render_template('gamereviews.html', reviews=mongo.db.reviews.find({"game_name" : game_name, "rating" : "2"}), game=mongo.db.games.find_one({"game_name": game_name}))
    
@app.route('/game_review/<game_name>/rating3')
def rating3(game_name):
    return render_template('gamereviews.html', reviews=mongo.db.reviews.find({"game_name" : game_name, "rating" : "3"}), game=mongo.db.games.find_one({"game_name": game_name}))
    
@app.route('/game_review/<game_name>/rating4')
def rating4(game_name):
    return render_template('gamereviews.html', reviews=mongo.db.reviews.find({"game_name" : game_name, "rating" : "4"}), game=mongo.db.games.find_one({"game_name": game_name}))
    
@app.route('/game_review/<game_name>/rating5')
def rating5(game_name):
    return render_template('gamereviews.html', reviews=mongo.db.reviews.find({"game_name" : game_name, "rating" : "5"}), game=mongo.db.games.find_one({"game_name": game_name}))
    
#When the users adds a review from a games gamereviews.html page, the game_name value is already selected
@app.route('/add_review/<game_name>')
def add_game_review(game_name):
    return render_template('addreview.html', games=mongo.db.games.find())

if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)