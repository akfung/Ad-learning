# dependencies
import pandas as pd
import ast
import json
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
from collections import Counter

ad_features = ['positivity','toxicity', 'insult', 'general'] #list of ML label categories and general category for all entries

#function for generating dictionaries of top words for graphing
def top_words(ad_df, unique_ad_df, unique=False):
    STOPWORDS.add('\n\nHe')
    STOPWORDS.add('')
    STOPWORDS.add('-')
    output_to_js = {}
    
    #set to df with duplicates by default. If unique == True then use df without duplicates
    df = ad_df
    if unique == True:
        df = unique_ad_df
    
    #loop through ad features to identify top words
    for feature in ad_features:
        
        if feature == 'general': #select the whole df for the 'general' feature
            text = df['AdText']
        else:
            text = df.loc[ad_df[feature]==1, 'AdText'] #select entries positive for feature
        
        #join all ad text into single string then split by spaces into list
        text = " ".join(str(description) for description in text).split(' ')

        #remove stopwords
        text = [word for word in text if not word in STOPWORDS]

        #use counter to grab most common words
        count_tuple = Counter(text).most_common(10)

        #write counts to dictionary
        count_dict = {}
        for entry in count_tuple:
            word, count = entry
            count_dict.update({word: count})
        
        
        words_key = f'{feature}TopWords'
        if unique == True:
            words_key = f'{feature}TopWordsUnique'
        
        #append the dictionary with count_dict
        output_to_js.update({words_key : count_dict})
    return(output_to_js)

#function for spending stats
def spending_values(ad_df, unique_ad_df, unique=False):
    
    #empty dict for writing json output
    output_to_js = {}
    
    #set to df with duplicates by default. If unique == True then use df without duplicates
    df = ad_df
    if unique == True:
        df = unique_ad_df
        
    #loop through features in ad_features    
    for feature in ad_features:
        
        if feature == 'general': #select the whole df for the 'general' feature
            spending_series = df['AdSpending']
        else:
            spending_series = df.loc[ad_df[feature]==1, 'AdSpending'] #select only entries positive for feature
        
        
        # create dict for spending amount categories
        spending_dict = spending_series.value_counts().sort_values(ascending=False).to_dict()
        
        spending_key = f'{feature}spending'
        if unique == True:
            spending_key = f'{feature}spendingUnique'

        # add $ to the start of each dollar value
        for key, value in spending_dict.items():
            spending_dict[key] = "$" + str(value)

        output_to_js.update({spending_key: spending_dict})
    return output_to_js

#function for impression stats
def impressions_values(ad_df, unique_ad_df, unique=False):
    
    #empty dict for writing json output
    output_to_js = {}
    
    #set to df with duplicates by default. If unique == True then use df without duplicates
    df = ad_df
    if unique == True:
        df = unique_ad_df
        
    #loop through features in ad_features    
    for feature in ad_features:
        
        if feature == 'general': #select the whole df for the 'general' feature
            impressions_series = df['Impressions']
        else:
            impressions_series = df.loc[ad_df[feature]==1, 'Impressions'] #select only entries positive for feature
        
        
        # create dict for spending amount categories
        impressions_dict = impressions_series.value_counts().sort_values(ascending=False).to_dict()
        
        impressions_key = f'{feature}Impressions'
        if unique == True:
            impressions_key = f'{feature}ImpressionsUnique'
        
        output_to_js.update({impressions_key: impressions_dict})
    return output_to_js