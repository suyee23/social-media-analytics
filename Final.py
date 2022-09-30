# -*- coding: utf-8 -*-
"""
Created on Fri May 21 18:11:06 2021

@author: jiaen
"""

# Description: This is a sentiment analysis program that parses the tweets fetched from Twitter using Python

import tweepy
from textblob import TextBlob
from wordcloud import WordCloud
import pandas as pd
import numpy as np
import re
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')

consumer_key = "zDPQ4jJBWt3zgCmXiv8iIA7Cx"
consumer_secret = "MgyMMzK3J7MQdKQORCwOutX3AaEwvq8dlopgZaYo6wvm9S7h3K"
access_key = "1390157511689265155-EyTwYk0Cq7ed1XIk8chWHujmrGkmkA"
access_secret = "0bfZ8k8HIyhMawNU4gPT7XBYDSXjjePXxV8fX5cLXht88"

# Create the authentication object
authenticate = tweepy.OAuthHandler(consumer_key,consumer_secret)

# Set the access token and access token secret
authenticate.set_access_token(access_key,access_secret)

# Create the API object while passing in the auth information
api = tweepy.API(authenticate, wait_on_rate_limit= True)

# Extract 100 tweets from the twitter username
posts = api.search(q = "coronavirus", count = 100, lang = "en", tweet_mode = "extended")
    
# Create a dataframe with a column called Tweets
df = pd.DataFrame([tweet.full_text for tweet in posts], columns = ['Tweets'])

# Clean Data
# Create a new data frame with a column called Tweets
df_cleaned = pd.DataFrame([tweet.full_text for tweet in posts], columns = ['Tweets'])

# Create a function to clean the tweets
def cleanTxt(text):
    text = re.sub(r'@[A-Z a-z 0-9]+','', text) # Removed @mentions
    text = re.sub(r'http\S+',' ', text) # Removed Hyperlink
    text = re.sub('[^A-Za-z0-9]+',' ', text) #Removed Special Characters
    text = re.sub(r'RT[\s]+','',text) # Removed Retweets
    return text

def remove_emoji(string):
    emoji_pattern = re.compile("["
                           u"\U0001F600-\U0001F64F"  # emoticons
                           u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                           u"\U0001F680-\U0001F6FF"  # transport & map symbols
                           u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           u"\U00002702-\U000027B0"
                           u"\U000024C2-\U0001F251"
                           "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', string)

# Cleaning the text by having the column'Tweets'
df_cleaned['Tweets'] = df_cleaned['Tweets'].apply(cleanTxt)
df_cleaned['Tweets'] = df_cleaned['Tweets'].apply(remove_emoji)

# Show the cleaned text
df_cleaned



# Plot the word cloud
allWords = ' '.join([twts for twts in df_cleaned['Tweets']])
wordCloud = WordCloud(width = 500, height = 300, background_color = 'white', random_state = 21, max_font_size = 119).generate(allWords)

plt.imshow(wordCloud, interpolation = "bilinear")
plt.axis('off')
plt.show()


# Create a new data frame 
df_Sentiment = df_cleaned

# Create a function to get the subjectivity(personal opinion rather than factual)
def getSubjectivity(text):
    return TextBlob(text).sentiment.subjectivity

# Create a function to get the polarity(positive, negative,neutral)
def getPolarity(text):
    return TextBlob(text).sentiment.polarity

# Create two new columns
df_Sentiment['Subjectivity'] = df_cleaned['Tweets'].apply(getSubjectivity)
df_Sentiment['Polarity'] = df_cleaned['Tweets'].apply(getPolarity)

#Show the new dataframe with new columns
df_Sentiment

# Create a new data frame for analysis
df_Result = df_Sentiment

# Create a function to compute the negative, neutral and positive analysis
def getAnalysis(score):
    if score < 0:
        return 'Negative'
    elif score == 0:
        return 'Neutral'
    else:
        return 'Positive'

df_Result['Analysis'] = df_Sentiment['Polarity'].apply(getAnalysis)

# Show the datafame of result
df_Result


# Plot scatter plot for the polarity and subjectivity
plt.figure(figsize=(8,6))
for i in range(0,df_Result.shape[0]):
    plt.scatter(df_Result['Polarity'][i], df_Result['Subjectivity'][i], color = 'Blue')
    
plt.title('Sentiment Analysis')
plt.xlabel('Polarity')
plt.ylabel('Subjectivity')
plt.show()

# Show the value counts by bar chart
df_Result['Analysis'].value_counts()

# Plot and visualize the counts
plt.title('Sentiment Analysis of Coronavirus past 100 Tweets')
plt.xlabel('Sentiment Variables')
plt.ylabel('Counts')
df_Result['Analysis'].value_counts().plot(kind='bar')
plt.show()


