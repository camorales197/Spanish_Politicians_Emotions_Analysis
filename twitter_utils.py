import tweepy
import os
from dotenv import load_dotenv
import numpy as np
import re
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from googletrans import Translator
import pandas as pd


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


#@st.cache()  # 👈 This function will be cached
def getting_tweets(authors, n_tweets, pages):
    authors_list = []
    tweets_list = []
    scores_list = []
    dates_list = []
    x = 3200

    for author in authors:
        print(author)

        tweets, dates, authors = list_tweets(author, n_tweets, pages)
        for t in tweets:
            text, sentiment = sentiment_analyzer_scores(t)
            tweets_list.append(text)
            scores_list.append(sentiment)
            x -= 1
            print(x)
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
    print(df)
    return df


def list_tweets(user_id, n_tweets, pages):
    api = auth_tweeter()

    tw = []
    dates = []
    author = []

    for page in range(pages):
        tweets = api.user_timeline("@" + user_id, count=n_tweets, tweet_mode='extended', page=page)

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
    #text = translator.translate(text=text).text
    #sentiment = analyser.polarity_scores(text)["compound"]
    sentiment = 0
    text = text
    return text, sentiment

def resample_df(data, freq='W'):
    df2 = data.copy()
    df2["Date"] = pd.to_datetime(df2['Date'])
    df2.set_index('Date', inplace=True)
    df2 = df2.groupby('Author').resample(freq).mean()
    df2.reset_index(inplace=True)
    return df2


authors = ['sanchezcastejon', 'pablocasado_', 'PabloIglesias', 'Santi_ABASCAL', 'InesArrimadas']
#authors = ['gabrielrufian']

colors = {"InesArrimadas": "rgb(249, 70, 0)",
          "Santi_ABASCAL": "rgb(80, 184, 47)",
          "PabloIglesias": "rgb(86, 40, 87)",
          "sanchezcastejon": "rgb(224, 53, 44)",
          "pablocasado_": "rgb(1, 72, 137)"}


translator = Translator()
analyser = SentimentIntensityAnalyzer()

