from flask import Flask, redirect, url_for, render_template, request
# import sqlalchemy

app = Flask(__name__)
acc = {"admin":"admin"}
data = [
    {
        "name":"BCIT",
        "city": "Vancouver",
        "address":"555 Seymour",
        "hours":"08:00 - 17:00",
        "link":"https://www.bcit.ca/",
        "phone":"(604) 434-5734",
        "type":"uni",
    },
    {
        "name":"BCIT",
        "city": "Burnaby",
        "address":"3700 Willingdon Ave",
        "hours":"08:00 - 17:00",
        "link":"https://www.bcit.ca/",
        "phone":"(604) 434-5734",
        "type":"uni",
    },
    {
        "name":"UBC",
        "city": "Vancouver",
        "address":"2329 West Mall",
        "hours":"07:00 - 16:00",
        "link":"https://www.ubc.ca/",
        "number":"(604) 822-2211",
        "type":"uni",
    },
]

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/vancouver")
def vancouver():
    return render_template("vancouver.html", locations = data)

@app.route("/burnaby")
def burnaby():
    return render_template("burnaby.html", locations = data)

@app.route("/surrey")
def surrey():
    return render_template("surrey.html", locations = data)

@app.route("/richmond")
def richmond():
    return render_template("richmond.html", locations = data)

@app.route("/coquitlam")
def coquitlam():
    return render_template("coquitlam.html", locations = data)

@app.route("/locations")
def locations():
    return render_template("locations.html", locations = data)

@app.route("/admin")
def admin():
    return render_template("admin.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def auth():
    user = request.form.get("user")
    password = request.form.get("password")
    if user in acc and password == acc[user]:
        return redirect("admin")
    else:
        return redirect("login")

if __name__ == "__main__":
    app.run(debug=True)
