import os
import pandas as pd
from flask import (
    Flask,
    render_template,
    jsonify,
    request,
    redirect)

from flask_sqlalchemy import SQLAlchemy
import ads_api #module for calling the facebook ads library API

#flask setup
app = Flask(__name__)

#set different database depending on dev or heroku database
ENV = 'dev'

if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:firefox@localhost/ad_learning'
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://rtecpnstgntqdo:38fb349af874ac157315e76e5af370df1c34b8afd280dfdf654768d68be75955@ec2-54-175-117-212.compute-1.amazonaws.com:5432/d3a8c7nhlm3gch'

#database setup
db = SQLAlchemy(app)

#class object for political_ads table
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
    #initialization functions
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
    #on load clear previous tables and populate the database with some ad results
    db.drop_all()
    # db.create_all()
    csv_data = pd.read_csv('../Data/20200511.csv') #read the csv to csv_data
    csv_data.to_sql('political_ads', db.engine) #write the pandas df to postgres df

    return render_template("index.html")



#route that goes to visualization page
@app.route("/visualization", methods=["GET"])
def visualization():
    _data = [{
        "type": "scattergeo",
        "locationmode": "USA-states",
        "lat": lat,
        "lon": lon,
        "text": hover_text,
        "hoverinfo": "text",
        "marker": {
            "size": 50,
            "line": {
                "color": "rgb(8,8,8)",
                "width": 1
            },
        }
    }]
    return render_template("ad_visualizations.html")

#route that adds to db
@app.route("/querryDB", methods=["GET", "POST"])
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

