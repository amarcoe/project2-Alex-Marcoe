import TMDB_API
import Wiki_API
import flask
import database
from flask_login import LoginManager

# from database import create_table, Person, db
from os import getenv

app = flask.Flask(__name__)
app.secret_key = getenv("secret_key")
# app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")

login_manager = LoginManager()

# db.init_app(app)
login_manager.init_app(app)

# create_table(app)


@app.route("/")
def login():
    return flask.render_template("login.html")


@app.route("/login", methods=["POST"])
def handle_login():
    form_data = flask.request.form  # This will give us all the form data from index
    username = form_data["username"]
    if authenticate_user(username):
        return flask.redirect(flask.url_for("index"))
    else:
        flask.flash(
            "That username doesn't exit, try typing it again or create an account."
        )
        return flask.redirect(flask.url_for("login"))


# 1.Login queries against database username
# 1. If username is in database continue
# 2. Else flash message
# 2.If user clicks create account
# 1. Query against database for username
# 2. If not in database
# 1.Add and continue
# 3. Else
# 1. flash message saying to login


@app.route("/index")
def index():
    movie_data = TMDB_API.choose_harcode_or_trending()
    wiki_page_url = Wiki_API.get_wiki_url(movie_data["title"], movie_data["year"])
    return flask.render_template(
        "index.html", movie_data=movie_data, wiki_page_url=wiki_page_url
    )


def authenticate_user(username):
    return username == "Alex"


app.run(debug=True)
