from flask import Flask, render_template
from flask_sock import Sock
from src.compounder import compound_investment_with_monthly_contributions as compound_df
import json
from utils import *

app = Flask(__name__, static_folder='static')
sock = Sock(app)

@app.route("/")
def home():
    context = {'title': "finance cookbook"}
    return render_template("home.html", context=context)
@app.route("/tutorials")
def tutorials():
    context = {'title': "finance cookbook"}
    return render_template("tutorials.html", context=context)

@app.route("/tutorial-diversification")
def diversification():
    stocks = ["MSFT", "RCL", "DIS", "PG", "AAPL", "MMM", "AXP", "BA", "LUV"]
    context = {"stocks" : [[stock] for stock in stocks]}
    stock_info = pd.read_csv("data/sp500_info.csv")
    for i, stock in enumerate(context["stocks"]):
        print(stock_info.loc[stock_info["Symbol"] == context["stocks"][i][0]]["GICS Sector"].values[0])
        context["stocks"][i] += [stock_info.loc[stock_info["Symbol"] == context["stocks"][i][0]]["GICS Sector"].values[0]]

    return render_template("diversification.html", context=context)

@sock.route('/diversification-ws')
def diversification_socket(ws):
    while True:
        message = ws.receive()
        ws.send(message)

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