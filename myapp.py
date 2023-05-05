from flask import Flask, redirect, url_for, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import secrets


# Create Flask App
app = Flask(__name__)

# SQL Alchemy Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///locations.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Create a database
db = SQLAlchemy(app)

#Initialize table
#Table consist of: name, location, hours of operation, contact information, link to website, type of location
class Locations(db.Model):
    id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    city = db.Column(db.String(100))
    address = db.Column(db.String(100), unique=True)
    hours = db.Column(db.String(100))
    link = db.Column(db.String(100))
    phone = db.Column(db.String(100))
    location_type = db.Column(db.String(100))

    def __init__(self, name, city, address, hours, link, phone, location_type):
        self.name = name
        self.city = city
        self.address = address
        self.hours = hours
        self.link = link
        self.phone = phone
        self.location_type = location_type

# Create a Form Class
class UserForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    city = StringField("City", validators=[DataRequired()])
    address = StringField("Address", validators=[DataRequired()])
    hours = StringField("Hours of Operation", validators=[DataRequired()])
    link = StringField("Link to Website", validators=[DataRequired()])
    phone = StringField("Phone Number", validators=[DataRequired()])
    location_type = StringField("Type of Location", validators=[DataRequired()])
    submit = SubmitField("Submit")


app.secret_key = secrets.token_hex(12)
acc = {"admin":"admin"}
# data = [
#     {
#         "name":"BCIT",
#         "city": "Vancouver",
#         "address":"555 Seymour",
#         "hours":"08:00 - 17:00",
#         "link":"https://www.bcit.ca/",
#         "phone":"(604) 434-5734",
#         "type":"uni",
#     },
#     {
#         "name":"BCIT",
#         "city": "Burnaby",
#         "address":"3700 Willingdon Ave",
#         "hours":"08:00 - 17:00",
#         "link":"https://www.bcit.ca/",
#         "phone":"(604) 434-5734",
#         "type":"uni",
#     },
#     {
#         "name":"UBC",
#         "city": "Vancouver",
#         "address":"2329 West Mall",
#         "hours":"07:00 - 16:00",
#         "link":"https://www.ubc.ca/",
#         "number":"(604) 822-2211",
#         "type":"uni",
#     },
# ]

@app.route("/")
def home():
    return render_template("index.html")

# Shows locations in Vancouver
@app.route("/vancouver")
def vancouver():
    vancouver_locations = Locations.query.filter_by(city="Vancouver").all()
    return render_template("vancouver.html", locations=vancouver_locations)

# Shows locations in Burnaby
@app.route("/burnaby")
def burnaby():
    burnaby_locations = Locations.query.filter_by(city="Burnaby").all()
    return render_template("burnaby.html", locations=burnaby_locations)

# Shows locations in Surrey
@app.route("/surrey")
def surrey():
    surrey_locations = Locations.query.filter_by(city="Surrey").all()
    return render_template("surrey.html", locations=surrey_locations)

# Shows locations in Richmond
@app.route("/richmond")
def richmond():
    richmond_locations = Locations.query.filter_by(city="Richmond").all()
    return render_template("richmond.html", locations=richmond_locations)

# Shows locations in Coquitlam
@app.route("/coquitlam")
def coquitlam():
    coquitlam_locations = Locations.query.filter_by(city="Coquitlam").all()
    return render_template("coquitlam.html", locations=coquitlam_locations)

# Shows locations in all locations
@app.route("/locations")
def locations():
    all_locations = Locations.query.all()
    return render_template("locations.html", locations=all_locations)

# Allow admin to delete locations
@app.route("/admin/delete/<int:location_id>")
def delete_location(location_id):
    location_to_delete = Locations.query.get_or_404(location_id)
    db.session.delete(location_to_delete)
    db.session.commit()
    return redirect(url_for("admin"))


@app.route("/admin", methods=["GET", "POST"])
def admin():
    if "admin" in session:
        form = UserForm()
        # Allowing admin to add locations
        if request.method == "POST" and form.validate_on_submit():
            name = form.name.data
            city = form.city.data
            address = form.address.data
            hours = form.hours.data
            link = form.link.data
            phone = form.phone.data
            location_type = form.location_type.data

            new_location = Locations(name=name, city=city, address=address, hours=hours, link=link, phone=phone, location_type=location_type)
            db.session.add(new_location)
            db.session.commit()

            return redirect(url_for("admin"))

        locations = Locations.query.all()
        return render_template("admin.html", form=form, locations=locations)
    return redirect("login")



@app.route("/login")
def login():
    # Check if admin is logged in through session cookie
    if "admin" in session:
        return redirect("admin")
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def auth():
    user = request.form.get("user")
    password = request.form.get("password")
    # Verify admin login entry and create log in session
    if user in acc and password == acc[user]:
        session["admin"] = user
        return redirect("admin")
    else:
        return redirect("login")

@app.route("/logout")
def logout():
    # If admin session exists, remove cookie to log out.
    if "admin" in session:
        session.pop("admin")
    return redirect("/")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
