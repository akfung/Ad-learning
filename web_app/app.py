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
    AdID = db.Column(db.Integer)
    AdURL = db.Column(db.String(200))
    AdText = db.Column(db.String(200))
    HostedPage = db.Column(db.String(200))
    Impressions = db.Column(db.String(200))
    Currency = db.Column(db.String(200))
    AdSpending = db.Column(db.String(200))
    toxicity = db.Column(db.Integer)
    identityAttack = db.Column(db.Integer)
    insult = db.Column(db.Integer)
    positivity = db.Column(db.Integer)
    #initialization functions
    def __init__(self, id, Ad_ID, Ad_URL, Ad_Text, Hosted_Page, Impressions, Currency, Ad_Spending):
        self.id = id
        self.AdID = AdID
        self.AdURL = AdURL
        self.AdText = AdText
        self.HostedPage = HostedPage
        self.Impressions = Impressions
        self.Currency = Currency
        self.AdSpending = AdSpending
        self.toxicity = toxicity
        self.identityAttack = identityAttack
        self.insult = insult
        self.positivity = positivity


# create route that renders index.html template
@app.route("/")
def home():
    #on load clear previous tables and populate the database with some ad results
    db.drop_all()
    db.create_all()
    csv_data = pd.read_csv('../Data/20200514.csv') #read the csv to csv_data
    csv_data.to_sql('political_ads', db.engine) #write the pandas df to postgres

    return render_template("index.html")

#route that goes to visualization page
@app.route("/visualization")
def visualization():
    return render_template("ad_visualizations.html")


# set up responding to api requests to postgres server
@app.route("/api/ads")
def api_response():
    #query database and return list of lists with results
    results = db.session.query(political_ads.AdID, political_ads.AdURL, political_ads.AdText, political_ads.HostedPage,\
        political_ads.Impressions, political_ads.Currency, political_ads.AdSpending, political_ads.toxicity, political_ads.insult, \
        political_ads.positivity).all()
    Ad_ID = [result[0] for result in results]
    Ad_URL = [result[1] for result in results]
    Ad_Text = [result[2] for result in results]
    Hosted_Page = [result[3] for result in results]
    Impressions = [result[4] for result in results]
    Currency = [result[5] for result in results]
    Spending = [result[6] for result in results]

    #the json responde to an API query from app.js, results are already in plotly format
    ad_data = [{
        "Ad_ID": Ad_ID,
        "Ad_URL": Ad_URL,
        "Ad_Text": Ad_Text,
        "Hosted_Page": Hosted_Page,
        "Impressions": Impressions,
        "Currency": Currency,
        "Spending": Spending
    }]

    return jsonify(ad_data) #return 
    



if __name__ == "__main__":
    app.run()

