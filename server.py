from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
from datetime import datetime

app = Flask(__name__)

app.secret_key = "35veowirfhu3o84,.'k;"

users={"bob":"bobpw", "jeff":"jeffpw"}


def getdb():
    conn = sqlite3.connect('db.sqlite3')
    conn.row_factory = sqlite3.Row
    return conn.cursor()


def login_user(username):
    c = getdb()
    c.execute(f'SELECT * FROM users WHERE username = :username', {"username": username})
    row = c.fetchone()
    return row


def load_messages():
    c = getdb()
    c.execute(f'SELECT messages.id, message, username, date FROM messages join users on users.id = messages.user_id')
    rows = c.fetchall()
    return rows


def post_messages(message, date, datetime_format):
    c = getdb()
    c.execute(f'INSERT INTO messages (message, user_id, date) VALUES (?,?,?)',
              (message, session["user_id"], date.strftime(datetime_format)))
    c.connection.commit()


def register_user(username, password):
    c = getdb()
    c.execute(f'INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
    c.connection.commit()


@app.route('/')
def index():

    username_incorrect = False
    password_incorrect = False

    if "password_incorrect" in session:
        password_incorrect = session["password_incorrect"]
        del session["password_incorrect"]

    if "username_incorrect" in session:
        username_incorrect = session["username_incorrect"]
        del session["username_incorrect"]

    return render_template("index.html", username_incorrect=username_incorrect, password_incorrect=password_incorrect)


@app.route('/chat', methods=["GET","POST"])
def chat():
    if "username" not in session:
        return redirect("/")

    username = session["username"]

    if request.method == "POST":

        message = request.form["message"]

        date = datetime.now()
        DATETIME_FORMAT = '%d/%m/%Y %H:%M'

        post_messages(message, date, DATETIME_FORMAT)

    rows = load_messages()

    return render_template("chat_page.html", username=username, rows=rows)


@app.route('/login', methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]

    row = login_user(username)

    if row is None:
        session["username_incorrect"] = True
        return redirect("/")

    if row["password"] != password:
        session["password_incorrect"] = True
        return redirect("/")

    session["username_incorrect"] = False
    session["username"] = username
    session["user_id"] = row["id"]
    session["password_incorrect"] = False
    return redirect(url_for("chat"))


@app.route('/register', methods=["GET","POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        register_user(username, password)

        return redirect("/")

    return render_template("register.html")


@app.route('/logout')
def logout():
    del session["username"]
    return redirect("/")


app.run(debug=True)

# http://127.0.0.1:5000/chat
# create separate functions for all the database code (refactoring) e.g. load messages, save messages, etc.
# make the date look nicer in the message