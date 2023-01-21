from flask import Flask, render_template

app = Flask(__name__, static_folder='static')

@app.route("/")
def home():
    context = {'title': "finance cookbook"}
    return render_template("compounding.html", context=context)