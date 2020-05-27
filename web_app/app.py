import os
import pandas as pd
from flask import (
    Flask,
    render_template,
    jsonify,
    request,
    redirect)

from web_app_pkgs import top_words, spending_values, impressions_values
from flask_sqlalchemy import SQLAlchemy

#flask setup
app = Flask(__name__)

#set different database depending on dev or heroku database
ENV = 'dev'

if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:firefox@localhost/ad_learning'
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://nkiddhmjdoixeq:3fc3f96ebda80d3c86b33a03de146c6d2d334adc6582772081e2e2a70c2e2814@ec2-52-71-55-81.compute-1.amazonaws.com:5432/d7jg23nlfme3nj'

#database setup and drop all tables on initialization
db = SQLAlchemy(app)
db.drop_all()

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


#on app load populate the database with ad results from csv
csv_data = pd.read_csv("https://ad-learning.s3-us-west-1.amazonaws.com/20200514.csv") #read the csv to csv_data
csv_data.to_sql('political_ads', db.engine, if_exists='replace') #write the pandas df to postgres

# create route that renders index.html templates
@app.route("/")
def home():
    return render_template("index.html")

#route that goes to visualization page
@app.route("/visualization")
def visualization():
    return render_template("ad_visualizations.html")

#render page for wordclouds
@app.route("/wordCloud")
def cloud():
    return render_template("ad_word_clouds.html")


# set up responding to api requests to postgres server
@app.route("/api/ads", methods=['GET', 'POST'])
def api_response():
    #query database and return list of lists with results
    results = db.session.query(political_ads.AdText, political_ads.Impressions, political_ads.AdSpending,\
        political_ads.toxicity, political_ads.insult, political_ads.positivity).all()

    #use query results w/ list interpretation to generate df
    ad_df = pd.DataFrame({
        'AdText' : [result[0] for result in results],
        'Impressions' : [result[1] for result in results],
        'AdSpending' : [result[2] for result in results],
        'toxicity' : [result[3] for result in results],
        'insult' : [result[4] for result in results],
        'positivity' : [result[5] for result in results]
    })

    #df with duplicates dropped. deprecated
    unique_ad_df = ad_df.drop_duplicates(subset = 'AdText', keep='first')

    #create dictionary with processed data dictionaries
    ad_data = {
        "TopWords" : top_words(ad_df, unique_ad_df),
        "TopWordsUnique" : top_words(ad_df, unique_ad_df, unique=True),
        "spending" : spending_values(ad_df, unique_ad_df),
        "spendingUnique" : spending_values(ad_df, unique_ad_df, unique=True),
        "Impressions" : impressions_values(ad_df, unique_ad_df),
        "ImpressionsUnique" : impressions_values(ad_df, unique_ad_df, unique=True)
    }

    return jsonify(ad_data) #return the ad_data dict as a json
    

if __name__ == "__main__":
    app.run()

