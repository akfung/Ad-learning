
# testing for posgresql insertion
from sqlalchemy import create_engine
import pandas as pd

# set different database depending on dev or heroku database
ENV = 'dev'

if ENV == 'dev':
    engine = create_engine(
        'postgresql://postgres:firefox@localhost/ad_learning', echo=False)
else:
    engine = create_engine(
        'postgres://nkiddhmjdoixeq:3fc3f96ebda80d3c86b33a03de146c6d2d334adc6582772081e2e2a70c2e2814@ec2-52-71-55-81.compute-1.amazonaws.com:5432/d7jg23nlfme3nj')

ad_df = pd.read_csv('current.csv')
# write the pandas df to postgres
ad_df.to_sql('political_ads', con=engine, if_exists='replace')
