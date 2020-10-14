from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template("index.html")

@app.route('/chat')
def chat():
    return render_template("chat_page.html", username=request.args.get("username"))

app.run(debug=True)

# http://127.0.0.1:5000/chat

