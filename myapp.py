from flask import Flask, redirect, url_for, render_template, request, session
from flask_sqlalchemy import SQLAlchemy 
from sqlalchemy.exc import IntegrityError
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
    name = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(100))
    address = db.Column(db.String(100))
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

# Allowing user to request a location
class RequestLocation(db.Model):
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

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/request-location", methods=["GET", "POST"])
def request_location():
    form = UserForm()
    if request.method == "POST" and form.validate_on_submit():
        name = form.name.data
        city = form.city.data
        address = form.address.data
        hours = form.hours.data
        link = form.link.data
        phone = form.phone.data
        location_type = form.location_type.data

        new_request = RequestLocation(name=name, city=city, address=address, hours=hours, link=link, phone=phone, location_type=location_type)
        db.session.add(new_request)
        db.session.commit()

        return redirect(url_for("request_location"))

    requests = RequestLocation.query.all()

    return render_template("request.html", form=form, requests=requests)

# Adding a request to the location database
@app.route("/user_data/add/<int:request_id>")
def add_request_to_location(request_id):
    request_to_add = RequestLocation.query.get_or_404(request_id)
    new_location = Locations(
        name=request_to_add.name,
        city=request_to_add.city,
        address=request_to_add.address,
        hours=request_to_add.hours,
        link=request_to_add.link,
        phone=request_to_add.phone,
        location_type=request_to_add.location_type
    )
    db.session.add(new_location)
    db.session.delete(request_to_add)
    db.session.commit()
    return redirect(url_for("user_data"))


# Allowing user to filer and search for locations
def get_filtered_locations(city=None):
    search_query = request.args.get("search_query")
    filter_type = request.args.get("filter_type")
    query = Locations.query

    if city:
        query = query.filter_by(city=city)

    if search_query:
        search_query = f"%{search_query.lower()}%"
        query = query.filter(Locations.name.ilike(search_query))
    elif filter_type:
        if filter_type == "Other":
            query = query.filter(Locations.location_type.notin_(["Cafe", "School", "Library"]))
        else:
            query = query.filter_by(location_type=filter_type)

    return query.all(), filter_type, search_query

@app.route("/vancouver")
def vancouver():
    locations, filter_type, search_query = get_filtered_locations(city="Vancouver")
    return render_template("vancouver.html", locations=locations, filter_type=filter_type, search_query=search_query)

@app.route("/burnaby")
def burnaby():
    locations, filter_type, search_query = get_filtered_locations(city="Burnaby")
    return render_template("burnaby.html", locations=locations, filter_type=filter_type, search_query=search_query)

@app.route("/surrey")
def surrey():
    locations, filter_type, search_query = get_filtered_locations(city="Surrey")
    return render_template("surrey.html", locations=locations, filter_type=filter_type, search_query=search_query)

@app.route("/richmond")
def richmond():
    locations, filter_type, search_query = get_filtered_locations(city="Richmond")
    return render_template("richmond.html", locations=locations, filter_type=filter_type, search_query=search_query)

@app.route("/coquitlam")
def coquitlam():
    locations, filter_type, search_query = get_filtered_locations(city="Coquitlam")
    return render_template("coquitlam.html", locations=locations, filter_type=filter_type, search_query=search_query)

@app.route("/locations")
def locations():
    locations, filter_type, search_query = get_filtered_locations()
    return render_template("locations.html", locations=locations, filter_type=filter_type, search_query=search_query)

@app.route("/user_data")
def user_data():
    if "admin" in session:
        requests = RequestLocation.query.all()
        return render_template("user_data.html", requests=requests)
    else:
        return redirect("login")

# Allow admin to delete locations
@app.route("/admin/delete/<int:location_id>")
def delete_location(location_id):
    location_to_delete = Locations.query.get_or_404(location_id)
    db.session.delete(location_to_delete)
    db.session.commit()
    return redirect(url_for("admin"))

# Routing for deleting requests
@app.route("/user_data/delete/<int:request_id>")
def delete_request(request_id):
    request_to_delete = RequestLocation.query.get_or_404(request_id)
    db.session.delete(request_to_delete)
    db.session.commit()
    return redirect(url_for("user_data"))



@app.route("/admin", methods=["GET", "POST"])
def admin():
    if "admin" in session:
        form = UserForm()
        # Allowing admin to add locations
        search_query = request.args.get("search_query")
        filter_type = request.args.get("filter_type")

        if search_query:
            search_query = f"%{search_query.lower()}%"
            locations = Locations.query.filter(Locations.name.ilike(search_query)).all()
        elif filter_type:
            if filter_type == "Other":
                locations = Locations.query.filter(Locations.location_type.notin_(["Cafe", "School", "Library"])).all()
            else:
                locations = Locations.query.filter_by(location_type=filter_type).all()
        else:
            locations = Locations.query.all()

        #removed form.validate_on_submit
        #[[NEEDS FIX: Handle case sensitivity ]]
        if request.method == "POST":
            name = form.name.data
            city = form.city.data
            address = form.address.data
            open_time = request.form.get("open")
            close_time = request.form.get("close")
            link = form.link.data
            phone = request.form.get("phone")
            location_type = form.location_type.data



            #Format Phone number
            if "-" in phone:
                processed_phone = phone
            else:
                phone_digits = [*phone]
                phone_digits.insert(3, "-")
                phone_digits.insert(7, "-")
                processed_phone = ''.join(phone_digits)
            #Format Hours of operation
            open_hours = f'{open_time} - {close_time}'
            new_location = Locations(name=name, city=city, address=address, hours=open_hours, link=link, phone=processed_phone, location_type=location_type)
            db.session.add(new_location)
            # Handle Integrity Error from duplicate location names/addresses added to the database.
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()
                return render_template("admin.html", form=form, locations=locations, filter_type=filter_type, search_query=search_query, error="Names and Addresses entered must be unique")
            return redirect("admin")

        return render_template("admin.html", form=form, locations=locations, filter_type=filter_type, search_query=search_query)
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
