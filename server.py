from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)

app.secret_key = "35veowirfhu3o84,.'k;"

@app.route('/')
def hello_world():
    return render_template("index.html")

messages=[]

@app.route('/chat', methods=["GET","POST"])
def chat():
    username = session["username"]
    if request.method == "POST":
        message=request.form["message"]
        message_info={"author":username, "message":message}
        messages.append(message_info)
    return render_template("chat_page.html", username=username, messages=messages)

@app.route('/login')
def login():
    username = request.args.get("username")
    session["username"] = username
    return redirect(url_for("chat"))


app.run(debug=True)

# http://127.0.0.1:5000/chat

#homework: get chat fully working (new username thing) sending msgs needs to work again
