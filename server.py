from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3



app = Flask(__name__)

app.secret_key = "35veowirfhu3o84,.'k;"

users={"bob":"bobpw", "jeff":"jeffpw"}


def getdb():
    conn = sqlite3.connect('db.sqlite3')
    conn.row_factory = sqlite3.Row
    return conn.cursor()

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


messages=[]

@app.route('/chat', methods=["GET","POST"])
def chat():
    if "username" not in session:
        return redirect("/")

    username = session["username"]

    if request.method == "POST":
        message=request.form["message"]
        message_info={"author":username, "message":message}
        messages.append(message_info)
    return render_template("chat_page.html", username=username, messages=messages)


@app.route('/login', methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]

    c = getdb()
    c.execute(f'SELECT * FROM users WHERE username = :username', {"username": username})
    row = c.fetchone()

    if row is None:
        session["username_incorrect"] = True
        return redirect("/")

    if row["password"] != password:
        session["password_incorrect"] = True
        return redirect("/")

    session["username_incorrect"] = False
    session["username"] = username
    session["password_incorrect"] = False
    return redirect(url_for("chat"))


@app.route('/register', methods=["GET","POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        c = getdb()
        c.execute(f'INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
        c.connection.commit()
        return redirect("/")

    return render_template("register.html")


@app.route('/logout')
def logout():
    del session["username"]
    return redirect("/")


app.run(debug=True)

# http://127.0.0.1:5000/chat
# add a registration page where you can register if you are a new user => insert new record into database that you can use to login later