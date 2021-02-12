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
@app.route("/get_index")
def get_index():
    genres = list(mongo.db.genres.find().sort("genre_name", 1))
    games = mongo.db.games.find()
    return render_template("index.html", games=games, genres=genres)


@app.route("/search", methods=["GET", "POST"])
def search():
    query = request.form.get("query")
    games = mongo.db.games.find(({"$text": {"$search": query}}))
    return render_template("games.html", games=games)


@app.route("/get_games")
def get_games():
    query = request.args.get("query")
    if query:
        games = mongo.db.games.find(({"$text": {"$search": query}}))
    else:
        games = mongo.db.games.find()
    return render_template("games.html", games=games)


@app.route("/register", methods=["GET", "POST"])
def register():
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
    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
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

    if session["user"]:
        return render_template("profile.html", username=username)

    return redirect(url_for("login"))


@app.route("/logout")
def logout():
    # remove user from session cookies
    flash("You have been logged out")
    session.pop("user")
    return redirect(url_for("login"))


@app.route("/add_game", methods=["GET", "POST"])
def add_game():
    if request.method == "POST":
        game = {
            "game_name": request.form.get("game_name"),
            "img_url": request.form.get("img_url"),
            "genre_name": request.form.get("genre_name"),
            "year": request.form.get("year"),
            "developer": request.form.get("developer"),
            "publisher": request.form.get("publisher"),
            "description": request.form.get("description"),
            "added_by": session["user"],
        }
        mongo.db.games.insert_one(game)
        flash("Game Added To Database")
        return redirect(url_for("get_games"))

    genres = mongo.db.genres.find().sort("genre_name", 1)
    return render_template("add_game.html", genres=genres)


@app.route("/edit_game/<game_id>", methods=["GET", "POST"])
def edit_game(game_id):
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

    game = mongo.db.games.find_one({"_id": ObjectId(game_id)})
    genres = mongo.db.genres.find().sort("genre_name", 1)
    return render_template("edit_game.html", game=game, genres=genres)


@app.route("/delete_game/<game_id>")
def delete_game(game_id):
    mongo.db.games.remove({"_id": ObjectId(game_id)})
    flash("Game Removed Sucessfully")
    return redirect(url_for("get_games"))



@app.route("/read_more/<game_id>")
def read_more(game_id):
    game = mongo.db.games.find_one({"_id": ObjectId(game_id)})
    return render_template("read_more.html", game=game)


@app.route("/get_genres")
def get_genres():
    genres = list(mongo.db.genres.find().sort("genre_name", 1))
    return render_template("genres.html", genres=genres)


@app.route("/add_genre", methods=["GET", "POST"])
def add_genre():
    if request.method == "POST":
        genre = {
            "genre_name": request.form.get("genre_name")
        }
        mongo.db.genres.insert_one(genre)
        flash("Genre Added Succesfully")
        return redirect(url_for("get_genres"))

    return render_template("add_genre.html")


@app.route("/edit_genre/<genre_id>", methods=["GET", "POST"])
def edit_genre(genre_id):
    if request.method == "POST":
        edit = {
            "genre_name": request.form.get("genre_name")
        }
        mongo.db.genres.update({"_id": ObjectId(genre_id)}, edit)
        flash("Genre Successfully Updated")
        return redirect(url_for("get_genres"))

    genre = mongo.db.genres.find_one({"_id": ObjectId(genre_id)})
    return render_template("edit_genre.html", genre=genre)


@app.route("/delete_genre/<genre_id>")
def delete_genre(genre_id):
    mongo.db.genres.remove({"_id": ObjectId(genre_id)})
    flash("Genre Deleted")
    return redirect(url_for("get_genres"))


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
