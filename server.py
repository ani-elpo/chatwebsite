from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)

app.secret_key = "35veowirfhu3o84,.'k;"

users={"bob":"bobpw", "jeff":"jeffpw"}

@app.route('/')
def hello_world():
    if "password_correct" in session:
        username = session["username"]
        password_correct = session["password_correct"]
    return render_template("index.html")

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

    if username in users and users[username] == password:
        session["username"] = username
        password_correct = True
        session["password_correct"] = password_correct
        return redirect(url_for("chat"))
    else:
        password_correct = False
        session["password_correct"] = password_correct
        return redirect("/")

@app.route('/logout')
def logout():
    del session["username"]
    return redirect("/")


app.run(debug=True)

# http://127.0.0.1:5000/chat

#homework: display "password incorrect" message on login page instead of just blank screen
# find a better way to store passwords?
