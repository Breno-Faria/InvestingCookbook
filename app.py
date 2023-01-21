from flask import Flask, render_template
from flask_sock import Sock

app = Flask(__name__, static_folder='static')
sock = Sock(app)

@app.route("/")
def home():
    context = {'title': "finance cookbook"}
    return render_template("index.html", context=context)

@app.route("/tutorial-diversification")
def diversify():
    return render_template("diversification.html")

@app.route("/tutorial-compounding")
def compound():
    data = [1,2, 4, 3, 4, 2]
    context = {'title': "finance cookbook"}
    return render_template("compounding.html", context=context, data=data)

@sock.route('/echo')
def echo_socket(ws):
    while not ws.closed:
        message = ws.receive()
        ws.send(message)










