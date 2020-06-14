from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from googletrans import Translator
import tweepy
import os
from dotenv import load_dotenv

load_dotenv()

consumer_key = os.environ.get("API-key")
consumer_secret = os.environ.get("API-secret-key")
access_token = os.environ.get("access-token")
access_token_secret = os.environ.get("access-token-secret")


auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)


translator = Translator()

text = translator.translate(text='esto es un test').text

analyser = SentimentIntensityAnalyzer()
a = analyser.polarity_scores(text)["compound"]

print("The test ",text, "has a sentiment ",a)


