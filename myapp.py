from flask import Flask, redirect, url_for, render_template

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/vancouver")
def vancouver():
    return "This will be the locations to study in Vancouver"

@app.route("/burnaby")
def burnaby():
    return "This will be the locations to study in Burnaby"

@app.route("/surrey")
def surrey():
    return "This will be the locations to study in Surrey"

@app.route("/richmond")
def richmond():
    return "This will be the locations to study in Richmond"

@app.route("/coquitlam")
def coquitlam():
    return "This will be the locations to study in Coquitlam"

@app.route("/locations")
def locations():
    return "This will be all the locations of the study spots in the lower mainland!"

if __name__ == "__main__":
    app.run()
