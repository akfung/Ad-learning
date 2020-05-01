import requests
from config import fb_key

params = {
    'search_terms': 'california',
    'fields': 'id,ad_snapshot_url,ad_creative_body,page_name,demographic_distribution,impressions,currency,spend', #no spaces between fields
    'ad_reached_countries': 'US', #countries where the ad is available
    'access_token': fb_key #access token
    }
    
base_url = 'https://graph.facebook.com/6.0/ads_archive?'

id = []
ad_snapshot_url = [] #url link to ad image
ad_creative_body = [] #text underneath ad
page_name = [] #name of page where ad is hosted
demographic_distribution = [] #age demographics
impressions = [] #essentially views
currency = [] #currency used to buy ad
spend = [] #spending on ad

response = requests.get(base_url, params = params).json()

for ad in response:
    print(ad)
