from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template("index.html")

messages=[]

@app.route('/chat', methods=["GET","POST"])
def chat():
    if request.method == "POST":
        username=request.form["username"]
        message=request.form["message"]
        message_info={"author":username, "message":message}
        messages.append(message_info)
    elif request.method == "GET":
        username=request.args.get("username")
    return render_template("chat_page.html", username=username, messages=messages)

app.run(debug=True)

# http://127.0.0.1:5000/chat

