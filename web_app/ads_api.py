#dependencies
import requests
import pandas as pd
from config import fb_key
import numpy as np
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
    
    def call_api(self, page_limit=2): #function to call api. page limit sets max num of pages to pull data from
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
            'Ad ID': self.id,
            'Ad URL': self.ad_snapshot_url,
            'Ad Text': self.ad_creative_body,
            'Hosted Page': self.page_name,
            'Impressions': self.impressions,
            'Currency': self.currency,
            'Ad Spending': self.spend
        })

        return results_df
    

        
