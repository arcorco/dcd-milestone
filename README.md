# Data Centric Milestone - Board Game Library

### Project Overview
The purpose of this project is to provide users with a place to store information about board games they or other users own and to leave reviews about 
board games already on the site. Users can browse through the website to see which games are rated highly and find out what other users think of the games.
The website creates a community for board game lovers to express their opinions about board games, add board games to the library to create an extenisive 
amount of games to peruse and to find out about games they may not have played before. The board games and their reviews are 
stored as collections in a MongoDB database.

### UX
![Wireframe1](/README-images/wireframe1.jpg)
![Wireframe2](/README-images/wireframe2.jpg)
* As a user who owns a board game which is not already in the library, I would want to add my board game to the library to increase the number of games available
to view and to allow other users to leave reviews for the game to find out what other people think about it.
* As a board game enthusiast, I would want to leave reviews on games in the library to help other users know whether a particular board game is good or not.
* As a user who is looking to purchase a new board game, I would want to browse a selection of games and view the reviews left on the games to decide 
which game was worth buying.
* As a user who wants to view a quick overview of information about board games, I would want to see an easy to understand visual representation of the information
in the library to make quick decisions about whether a board game is good or not.

### Website Tutorial and Features
1. On the Board Game Library home page the user can view a carousel of the games in the library an click on the "VIEW GAME INFORMATION AND REVIEWS" button to view more information about the game and the reviews left for the game.
    * This button takes the user to the information page about the game and shows the reviews other users have left for the game. On the page the user can edit information about the game and delete the game from the library. The user can also add a review for this particular game by clicking the "ADD REVIEW" button, where they will be redirected to a form for them to fill in with their review . The user can also sort the reviews left on the game by most recently added, in order of 5 star reviews to 1 star review, or in order of 1 star reviews up to 5 star reviews. The user can also filter the reviews shown to only view 5 star, 4 star, 3 star, 2 star, or 1 star reviews.
2. From the nav bar, the user can be directed to the dashboard page which shows charts from MongoDB Charts. Here the user can view a visual representation of selected data about the board games, including a circle chart representing the number of reviews left on each game that recommend the game, a bar chart comparing the average ratings of each game, and a heat map the represent the number of reviews left on each game (grouped by their rating).
3. From the nav bar, the user can then be directed to view a directory of all games in the library with all of the information about the games. The user can sort the directory to view the games in alphabetical order, most recently added, and highest rated to lowest rated. The user can also filter the games shown to view games of an average rating of at least 2 stars, 3 stars, 4 stars, or 5 stars. In the directory, the user can also click the "EDIT" button for a game which redirects them to a form, where all values in the form are already filled in with the current information stored in the database, for the user to edit the information about the game. The user can also click on the "REVIEWS" button which takes the user to the information page about the game (the same page that the "VIEW GAME INFORMATION AND REVIEWS" button from the home page directs the user to).
4. From the nav bar, the user can add a game to the library. The user is directed to a page with a form for them to fill in with information about the game. In this form the user can also upload an image file for the game, or if the don't a default image will be used to show the game. The user clicks the "ADD GAME" buttons to create the game document in the MongoDB.
5. From the nav bar, the user can finally add a review for any game in the libary. The user is directed to a form for them to fill in with their review. This is the same form the user is linked to from the "ADD REVIEW" button on a game's information page, but this time the user does not have a pre-selected game chosen for them. The user clicks the "ADD REVIEW" button to create the review document in the MongoDB database.

#### Some more features to note:
* The MongoDB Charts are automatically updated when new information is added to the database.
* When a user wants to edit a game or a review, they are directed to the Edit Game/ Edit Review form, where all of the values are already filled in from the information already in the database regarding the document they wish to change.
* When a user wishes to add a review from a games information page, the Game Name field is already filled in with the particular game page they were directed from.
* When a user wishes to delete a game or a review, a modal pops up as a confirmation to ensure the user wishes to continue with the deletion.

#### Features To Implement
###### User Login
Currently any user on the website can edit and delete any of the games and reviews that are currently in the library. I would like to implement a user login
system where a user must login in to the website and then can only edit and delete the reviews and games they added to the website.

###### Filter and Sort
When a user filters or sorts a selection, the games/reviews are reset and then filtered/sorted from the whole collection each time. I would like to improve this
feature such that a user can combine the filters and a sort. For example, a user could sort the games into alphabetical order, then filter them to show games
with an average rating of at least 3 star and the result would still be shown in alphabetical order.

###### Search Bar
Although users can sort and filter the collections shown, I would like to implement a search feature where users can search for a game and be directed to that games 
information page if the game is in the library, or shown an error message if the game doesn't currently exist in the database.

### Technologies Used
* HTML5
* CSS
* JavaScript
* [jQuery v 3.4.1](https://code.jquery.com/) 
* This website was built with Flask frameworks, so Python was used to build the backend of the project.
* [MongoDB](https://www.mongodb.com/) was the database chosen to hold the data.
* [MongoDB Charts](https://www.mongodb.com/products/charts) were used to visualise the data.
* PyMongo was used to work with the MongoDB database.
* [Materialize](https://materializecss.com/) was used to build and style the website.
* [slick](https://kenwheeler.github.io/slick/) carousel used to showcase games on the home page.
* Chrome Developer Tools used for debugging, live-testing, styling and responsiveness.
* [Favicon.io](https://favicon.io/)

### Testing
The website was tested extensivley through many different means. MongoDB was used to check which key, values pairs were being added and updated to documents
in the database. This allowed me to ensure that with each form filled out on the website, there were no stray values being added. The aggregation section in MongoDb
when viewing the collections was especially helpful in figuring how best to sort and filter the collections. All of the forms in the website
are validated via JavaScript code (credit: [Form Validation Using JavaScript](https://www.formget.com/form-validation-using-javascript/)), ensuring that no fields
may be left empty (except for the "Add Image" field when a user is adding a game, as a default image will be used instead if they don't upload one) and a user 
cannot fill a field in with characters if it must be filled in with numbers. I also carried out a lot of manual testing on the website, for example:

1. Add a review from a game page (e.g. Monopoly)
    1. Go to a games information page, either via the carousel on the home page (find Monopoly and click the "VIEW GAME INFORMATION AND REVIEWS" button), or the directory under "All Games" (find Monopoly and click the "REVIEWS" button).
    2. Now directed to the Add Review page, the Game Name field is already selected with Monopoly
    3. Try to submit the form, error occurs and the message "Please input a Review" is shown beneath the Review field
    4. Fill in a review, try to submit form, error occurs and the message "Please choose a Rating out of 5" is shown beneath the Rating field
    5. Choose a rating out of 5 and submit form. No error occurs. 
    6. View the game page for Monopoly and see that the "Average Rating" for the game has been updated, and the new review can now be seen.

2. Delete a game
    1. Choose a game to be deleted and go to that games information page
    2. Click the "DELETE" button
    3. A modal pops up asking whether the user is sure they would like to delete the game
    4. If the user clicks "DON"T DELETE" this modal disappears and the user is still on the game's information page
    5. If the user clicks delete, they are redirected to the All Games directory page and the game they deleted is no longer there
    
3. Add a game
    1. Click on the Add Game button on the nav bar
    2. The user is directed to the Add Game form with all fields empty
    3. Try to submit the form, error occurs and the message "Please input a Game Name" is shown beneath the Game Name field
    4. Fill in a game name in the Game Name field and try to submit the form, error occurs and the message "Please input a Description" is shown beneath the Game Description field
    5. Fill in a description in the Game Description field and try to submit the form, error occurs and the message "Please input a Manufacturer" is shown beneath the Manufacturer field
    6. Fill in a manufacturer in the Manufacturer field and try to submit the from, error occurs and the message "Please input numbers only" is shown beneath the Minimum Number of Players field
    7. Write "two" and "four" in the Minimum Number of Players and Maximum Number of player fields respectively and try to submit the from, error occurs and the message "Please input numbers only" is shown beneath the Minimum Number of Player field
    8. Input "2" and "four" in the Minimum Number of Players and Maximum Number of player fields respectively and try to submit the form, error occurs and the message "Please input numbers only" is shown beneath the Minimum Number of Player field
    9. Input "2" and "4" in the Minimum Number of Players and Maximum Number of player fields respectively and try to submit the form, error occurs and the message "Please input numbers only. If the game has no recommended minimum age, please input 0" is shown beneath the Minimum Age field
    10. Input "ten" in the Minimum Age field and try to submit the form, error occurs and the message "Please input numbers only. If the game has no recommended minimum age, please input 0" is shown beneath the Minimum Age field
    11. Input "10" in the Minimum Age field and try to submit the form
    12. Form submitted successfully (whether an image is uploaded or not) and the game can be seen under the All Games tab and in the carousel on the home page

The responsiveness of the website on different viewport widths was tested throughout with Developer Tools and the element style section was used to make any alterations to the layout before
changing my style.css file. The website has also been tested on Safari, Chrome and Firefox and the deployed version has been tested on MacBook and iPhone X.

All HTML and CSS files validated via (https://www.w3.org/).

JavaScript validated via (https://jshint.com/).

### Deployment

This website was deployed to Heroku. I pushed my repository to GitHub, then buil an app on Heroku and connected it to GitHub so that an repository pushes to GitHub would automatically
deploy to Heroku. The environment variables used are the same in the deployed version as in the development version, held in an env.py file or as Heroku Config
Var. To deploy to Heroku I also included a requirements.txt and a Procfile.

To run the code locally,  install all packages from the requirements.txt file. Then copy files from the "static" directory, "templates" directory and app.py.
Any environment variables would need changing to match local information.

### Credits
The background image on the homepage is from (https://pixabay.com/photos/board-games-games-gesellschaftsspiel-460340/).

Chess board default image is from (http://chesssetup.com/), and I added the "DEFAULT IMAGE" text.

##### Acknowledgements
[Pretty Printed](https://www.youtube.com/watch?v=DsgAuceHha4) on YouTube, in particular their video on saving files to a MongoDB database.
