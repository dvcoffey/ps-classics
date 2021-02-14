import os
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
if os.path.exists("env.py"):
    import env

app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)


@app.route("/")
@app.route("/index")
def index():
    """
    List items by most recently added to database
    List items by most page views
    List genres to browse by genre
    Return index.html
    """
    recents = list(mongo.db.games.find().sort("_id", -1).limit(4))
    views = list(mongo.db.games.find().sort("page_views", -1).limit(4))
    genres = list(mongo.db.genres.find().sort("genre_name", 1))
    return render_template(
        "index.html", recents=recents, views=views, genres=genres)


@app.route("/games")
def games():
    """
    Find games with search query if field has value
    Else find all games
    Return games.html
    """
    query = request.args.get("query")
    if query:
        games = mongo.db.games.find(
            ({"$text": {"$search": query}})).sort("_id", -1)
    else:
        games = mongo.db.games.find().sort("_id", -1)
    return render_template("games.html", games=games, query=query)


@app.route("/details/<game_id>")
def details(game_id):
    '''
    Find game by game_id
    Return game-details.html
    '''
    game = mongo.db.games.find_one({"_id": ObjectId(game_id)})
    mongo.db.games.update_one(
        {"_id": ObjectId(game_id)}, {'$inc': {'page_views': +1}})
    return render_template("game-details.html", game=game)


@app.route("/register", methods=["GET", "POST"])
def register():
    # register new user to database
    if request.method == "POST":
        # check if username already exists in database
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            flash("Username already exists")
            return redirect(url_for("register"))

        register = {
            "username": request.form.get("username").lower(),
            "password": generate_password_hash(request.form.get("password"))
        }
        mongo.db.users.insert_one(register)

        # put new user into 'session' cookie
        session["user"] = request.form.get("username").lower()
        flash("Registration Succesful!")
        return redirect(url_for("profile", username=session["user"]))

    # If user already exists
    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():

    # log in existing user
    if request.method == "POST":

        # check if username exists in db
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            # ensure hashed password matches user input
            if check_password_hash(
                existing_user["password"], request.form.get("password")):
                    session["user"] = request.form.get("username").lower()
                    flash("Welcome, {}".format(
                        request.form.get("username")))
                    return redirect(url_for(
                        "profile", username=session["user"]))
            else:
                # invalid password match
                flash("Incorrect Username and/or Password")
                return redirect(url_for("login"))

        else:
            # username doesn't exist
            flash("Incorrect Username and/or Password")
            return redirect(url_for("login"))

    return render_template("login.html")


@app.route("/profile/<username>", methods=["GET", "POST"])
def profile(username):
    # grab session user's username from the database
    username = mongo.db.users.find_one(
        {"username": session["user"]})["username"]

    '''
    list games added to database by user
    return profile.html
    '''
    if session["user"]:
        games = list(mongo.db.games.find(
            {"added_by": session["user"]}).sort("_id", -1))
        return render_template("profile.html", username=username, games=games)

    return redirect(url_for("login"))


@app.route("/logout")
def logout():
    # remove user from session cookies
    flash("You have been logged out")
    session.pop("user")
    return redirect(url_for("login"))


@app.route("/add_game", methods=["GET", "POST"])
def add_game():
    '''
    request input fields from form data
    add new game to the database
    return games.html
    '''
    if request.method == "POST":
        # time_stamp stores datetime to a string to by used by database
        game = {
            "game_name": request.form.get("game_name"),
            "img_url": request.form.get("img_url"),
            "genre_name": request.form.get("genre_name"),
            "year": request.form.get("year"),
            "developer": request.form.get("developer"),
            "publisher": request.form.get("publisher"),
            "description": request.form.get("description"),
            "added_by": session["user"]
        }
        mongo.db.games.insert_one(game)
        flash("Game Added To Database")
        return redirect(url_for("games"))

    # retrieves genres for dropdown selector
    genres = mongo.db.genres.find().sort("genre_name", 1)
    return render_template("add-game.html", genres=genres)


@app.route("/edit_game/<game_id>", methods=["GET", "POST"])
def edit_game(game_id):
    '''
    request input fields from form data
    update an existing game in the database
    return games.html
    '''
    if request.method == "POST":
        edit = {
            "game_name": request.form.get("game_name"),
            "img_url": request.form.get("img_url"),
            "genre_name": request.form.get("genre_name"),
            "year": request.form.get("year"),
            "developer": request.form.get("developer"),
            "publisher": request.form.get("publisher"),
            "description": request.form.get("description"),
            "added_by": session["user"],
        }
        mongo.db.games.update({"_id": ObjectId(game_id)}, edit)
        flash("Game Edited")

    # find game by ObjectId
    game = mongo.db.games.find_one({"_id": ObjectId(game_id)})
    # retrieves genres for dropdown selector
    genres = mongo.db.genres.find().sort("genre_name", 1)
    return render_template("edit-game.html", game=game, genres=genres)


@app.route("/delete_game/<game_id>")
def delete_game(game_id):
    mongo.db.games.remove({"_id": ObjectId(game_id)})
    flash("Game Removed Sucessfully")
    return redirect(url_for("games"))


@app.route("/genres")
def genres():
    '''
    retrieve list of genres in database
    return genres.html
    '''
    genres = list(mongo.db.genres.find().sort("genre_name", 1))
    return render_template("genres.html", genres=genres)


@app.route("/add_genre", methods=["GET", "POST"])
def add_genre():
    '''
    request input fields from form data
    add new genre to the database
    return add-genre.html
    '''
    if request.method == "POST":
        genre = {
            "genre_name": request.form.get("genre_name")
        }
        mongo.db.genres.insert_one(genre)
        flash("Genre Added Succesfully")
        return redirect(url_for("genres"))

    # if form input is cancelled
    return render_template("add-genre.html")


@app.route("/edit_genre/<genre_id>", methods=["GET", "POST"])
def edit_genre(genre_id):
    '''
    request input fields from form data
    update an existing genre in the database
    return genres.html
    '''
    if request.method == "POST":
        edit = {
            "genre_name": request.form.get("genre_name")
        }
        mongo.db.genres.update({"_id": ObjectId(genre_id)}, edit)
        flash("Genre Successfully Updated")
        return redirect(url_for("genres"))

    # if form input is cancelled
    genre = mongo.db.genres.find_one({"_id": ObjectId(genre_id)})
    return render_template("edit-genre.html", genre=genre)


@app.route("/delete_genre/<genre_id>")
def delete_genre(genre_id):
    mongo.db.genres.remove({"_id": ObjectId(genre_id)})
    flash("Genre Deleted")
    return redirect(url_for("genres"))


@app.route("/filter_genre/<genre_name>", methods=["GET", "POST"])
def filter_genre(genre_name):
    '''
    retrieve games from database that contain a specific genre
    return games.html with filter applied
    '''
    games = list(mongo.db.games.find({"genre_name": genre_name}))
    return render_template("games.html", games=games)



@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html', title='404'), 404


@app.errorhandler(500)
def internal_server(error):
    return render_template('500.html', title='500'), 500


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=False)
