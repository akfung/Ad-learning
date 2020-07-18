#This script queries the fb ad library api for 10k results into a pandas df. The ads in the df are processed with the trained RNN using settings and tokenizers in the ml_settings folder. Ads are labeled with a 1 in the column corresponding to the ad group if positively labeled. The df is saved to a csv.

#dependencies
import requests
import pandas as pd
from config import fb_key
import numpy as np
import tensorflow as tf
import tensorflow_datasets as tfds
import ast
import json
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
from collections import Counter
#set attributes to search for and pull
ad_attributes = ['id', 'ad_snapshot_url', 'ad_creative_body', 'page_name', 'demographic_distribution', 'impressions', 'currency', 'spend']


# fb_ad_api class object for querying api
class fb_ad_api:
    def __init__(self, search='""'):
        #initialize object to contain lists for ad attributes
        self.id = []
        self.ad_snapshot_url = []
        self.ad_creative_body = []
        self.page_name = []
        self.demographic_distribution = []
        self.impressions = []
        self.currency = []
        self.spend = []
        #list comprehension from ad_attributes list to set returned attributes
        self.params = {
            'fields': ','.join(attribute for attribute in ad_attributes), 
            'ad_reached_countries': 'US', #countries where the ad is available
            'access_token': fb_key, #access token
            # 'ad_active_status': 'ALL',
            'limit': 100 #results per page
            }
        self.params.update({'search_terms': search}) #add search term to params if one is provided
        self.base_url = 'https://graph.facebook.com/v6.0/ads_archive?' #set base API URL
        self.ad_attributes = ['id', 'ad_snapshot_url', 'ad_creative_body', 'page_name', 'demographic_distribution', 'impressions', 'currency', 'spend']
    
    def call_api(self, page_limit=10): #function to call api. page limit sets max num of pages to pull data from
        page_counter = 1
        url = self.base_url

        
        while page_counter <= page_limit:
            print('Pulling page:' + str(page_counter)) # so you can know what's up
            #only include parameters for api call on page 1
            if page_counter == 1:
                response = requests.get(url, params = self.params).json()
            else:
                response = requests.get(url).json()
                
            results = response['data']
            
            for ad in results: #loop through each ad in api response page and append to attribute lists
                for attr in ad_attributes: #loop through each ad attribute and append to a list if present. Appends NaN if not present
                    if f'{attr}' in ad:
                        getattr(self, f'{attr}').append(ad[f'{attr}'])
                    else:
                        getattr(self, f'{attr}').append(np.nan)
            
            # break the loop if there isn't another page        
            if not(response['paging']['next']):
                break

            # set next api url according to paginated response    
            url = response['paging']['next']
            page_counter += 1
            

    # make pandas df
    def make_df(self):
        results_df = pd.DataFrame({
            'AdID': self.id,
            'AdURL': self.ad_snapshot_url,
            'AdText': self.ad_creative_body,
            'HostedPage': self.page_name,
            'Impressions': self.impressions,
            'Currency': self.currency,
            'AdSpending': self.spend
        })

        return results_df
    
#call the API and get 10 pages of 100 results each
ad_results = fb_ad_api()
ad_results.call_api(page_limit=100)
ad_df = ad_results.make_df()
        
# change upper/lower bound data entries to just upper_bound value
def remove_dict(sample):
    sample_dict = ast.literal_eval(str(sample))
    return sample_dict['upper_bound']
ad_df['Impressions'] = ad_df['Impressions'].map(remove_dict)
ad_df['AdSpending'] = ad_df['AdSpending'].map(remove_dict)

# list of ML features to reference
ad_features = ['positivity','toxicity','identityAttack', 'insult']
#padding function

def pad_to_size(vec, size):
  zeros = [0] * (size - len(vec))
  vec.extend(zeros)
  return vec

#function to return a ML prediction from text
def sample_predict(sample_pred_text):
    #encode sample
    encoded_sample_pred_text = tokenizer.encode(sample_pred_text) 
    encoded_sample_pred_text = pad_to_size(encoded_sample_pred_text, 64)
    encoded_sample_pred_text = tf.cast(encoded_sample_pred_text, tf.float32)
    predictions = model.predict(tf.expand_dims(encoded_sample_pred_text, 0))

    return (predictions)

# mapping function for the prediction values
def binary_label(prediction):
    if prediction >= 0.5:
        return 1
    return 0

#loop for each of the ad feature models
for feature in ad_features:
    print(f'processing {feature}')
    #set specific tokenizer if doing positivity predictions
    if feature == 'positivity':
        tokenizer = tfds.features.text.SubwordTextEncoder.load_from_file('../ml_settings/positivity_large_tokenizer')
    else:
        tokenizer = tfds.features.text.SubwordTextEncoder.load_from_file('../ml_settings/large_tokenizer')
    #load model
    model = tf.keras.models.load_model(f'../ml_settings/{feature}_rnn.h5')

    #map predictions to new column
    ad_df[feature] = ad_df['AdText'].map(lambda x: binary_label(sample_predict(str(x))))

#add dummy ids to ensure a column for primary keys
ad_df['dummy_id'] = range(1, len(ad_df) + 1)
ad_df = ad_df.drop_duplicates(subset = 'dummy_id', keep='first')

#save df to csv
ad_df.to_csv('../Data/20200528.csv')