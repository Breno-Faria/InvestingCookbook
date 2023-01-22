from flask import Flask, render_template
from flask_sock import Sock
from src.compounder import compound_investment_with_monthly_contributions as compound_df
import json

app = Flask(__name__, static_folder='static')
sock = Sock(app)

@app.route("/")
def home():
    context = {'title': "finance cookbook"}
    return render_template("home.html", context=context)

@app.route("/tutorial-diversification")
def diversify():
    return render_template("diversification.html")

@app.route("/tutorial-compounding")
def compound():
    data = [1,2, 4, 3, 4, 2]
    context = {'title': "finance cookbook"}
    return render_template("compounding.html", context=context, data=data)

# rename this for compounding
@sock.route('/compound-ws')
def compound_socket(ws):
    while True:
        message = ws.receive()
        message = [int(val) for val in message.split(",")]
        ts_compounding = compound_df(message[1], message[0]/100, 30,  message[2]).to_json(orient='index')
        ws.send(ts_compounding)


@app.route("/about-us")
def about():
    return render_template("aboutus.html")