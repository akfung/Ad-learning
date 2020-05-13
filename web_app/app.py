import os
from flask import (
    Flask,
    render_template,
    jsonify,
    request,
    redirect)

from flask_sqlalchemy import SQLAlchemy

#flask setup
app = Flask(__name__)

#set different database depending on dev or local database
ENV = 'dev'

if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:firefox@localhost/ad_learning'
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://rtecpnstgntqdo:38fb349af874ac157315e76e5af370df1c34b8afd280dfdf654768d68be75955@ec2-54-175-117-212.compute-1.amazonaws.com:5432/d3a8c7nhlm3gch'

#database setup
db = SQLAlchemy(app)

class political_ads(db.Model):
    __tablename__ = 'political_ads'
    id = db.Column(db.Integer, primary_key=True)
    Ad_ID = db.Column(db.Integer)
    Ad_URL = db.Column(db.String(200))
    Ad_Text = db.Column(db.String(200))
    Hosted_Page = db.Column(db.String(200))
    Impressions = db.Column(db.String(200))
    Currency = db.Column(db.String(200))
    Ad_Spending = db.Column(db.String(200))

    def __init__(self, id, Ad_ID, Ad_URL, Ad_Text, Hosted_Page, Impressions, Currency, Ad_Spending):
        self.id = id
        self.Ad_ID = Ad_ID
        self.Ad_URL = Ad_URL
        self.Ad_Text = Ad_Text
        self.Hosted_Page = Hosted_Page
        self.Impressions = Impressions
        self.Currency = Currency
        self.Ad_Spending = Ad_Spending


# create route that renders index.html template
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/send", methods=["GET", "POST"])
def send():
    if request.method == "POST":
        name = request.form["petName"]
        lat = request.form["petLat"]
        lon = request.form["petLon"]

        pet = Pet(name=name, lat=lat, lon=lon)
        db.session.add(pet)
        db.session.commit()
        return redirect("/", code=302)

    return render_template("form.html")



if __name__ == "__main__":
    app.run()

