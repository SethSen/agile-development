from flask import Flask, redirect, url_for, render_template
# import sqlalchemy

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/vancouver")
def vancouver():
    return render_template("vancouver.html")

@app.route("/burnaby")
def burnaby():
    return render_template("burnaby.html")

@app.route("/surrey")
def surrey():
    return render_template("surrey.html")

@app.route("/richmond")
def richmond():
    return render_template("richmond.html")

@app.route("/coquitlam")
def coquitlam():
    return render_template("coquitlam.html")

@app.route("/locations")
def locations():
    return render_template("locations.html")

@app.route("/admin")
def admin():
    return render_template("admin.html")

if __name__ == "__main__":
    app.run(debug=True)
