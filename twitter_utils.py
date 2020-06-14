import tweepy
import os
from dotenv import load_dotenv
import numpy as np
import re
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from googletrans import Translator
import pandas as pd
import streamlit as st


def auth_tweeter():
    load_dotenv()

    consumer_key = os.environ.get("API-key")
    consumer_secret = os.environ.get("API-secret-key")
    access_token = os.environ.get("access-token")
    access_token_secret = os.environ.get("access-token-secret")

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    return api


def list_tweets(user_id, count, prt=False):
    api = auth_tweeter()
    tweets = api.user_timeline(
        "@" + user_id, count=count, tweet_mode='extended')

    tw = []
    dates = []
    author = []

    for t in tweets:
        tw.append(t.full_text)
        dates.append(t.created_at)
        author.append(user_id)
    tw_clean = clean_tweets(tw)
    return tw_clean, dates, author


def remove_pattern(input_txt, pattern):
    r = re.findall(pattern, input_txt)
    for i in r:
        input_txt = re.sub(i, '', input_txt)
    return input_txt


def clean_tweets(lst):
    # remove twitter Return handles (RT @xxx:)
    lst = np.vectorize(remove_pattern)(lst, "RT @[\w]*:")
    # remove twitter handles (@xxx)
    lst = np.vectorize(remove_pattern)(lst, "@[\w]*")
    # remove URL links (httpxxx)
    lst = np.vectorize(remove_pattern)(lst, "https?://[A-Za-z0-9./]*")
    # remove URL links (httpxxx)
    lst = np.vectorize(remove_pattern)(lst, "https*")
    # remove special characters, numbers, punctuations (except for #)
    lst = np.core.defchararray.replace(lst, "[^a-zA-Z#]", " ")
    return lst


def sentiment_analyzer_scores(text):
    text = translator.translate(text=text).text
    sentiment = analyser.polarity_scores(text)["compound"]
    return text, sentiment

@st.cache  # 👈 This function will be cached
def getting_tweets(authors, n_tweets):
    authors_list = []
    tweets_list = []
    scores_list = []
    dates_list = []

    for author in authors:
        tweets, dates, authors = list_tweets(author, n_tweets)
        for t in tweets:
            text, sentiment = sentiment_analyzer_scores(t)
            tweets_list.append(text)
            scores_list.append(sentiment)
        for d in dates:
            dates_list.append(d)
        for a in authors:
            authors_list.append(a)

    data = {'Author': authors_list,
            'Date': dates_list,
            'Tweet': tweets_list,
            'Score': scores_list
            }

    df = pd.DataFrame(data, columns=['Author', 'Date', 'Tweet', 'Score'])
    return df


translator = Translator()
analyser = SentimentIntensityAnalyzer()

