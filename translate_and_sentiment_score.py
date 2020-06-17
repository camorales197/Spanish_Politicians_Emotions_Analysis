import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from googletrans import Translator


def translate(text):
    try:
        text_translated = translator.translate(text=text).text
        return text_translated
    except:
        print("Error translating", text)
        return None


def sentiment_analyzer_scores(text):
    try:
        sentiment = analyser.polarity_scores(text)["compound"]
        return sentiment
    except:
        print("Error calculating sentiment", text)
        return None


translator = Translator()
analyser = SentimentIntensityAnalyzer()

df = pd.read_csv("tweets.csv", usecols=["Author", "Date", "Tweet"],
                 dtype={'Author': object, 'Date': object, 'Tweet': object})

df["Tweet_English"] = df.apply(lambda x: translate(x['Tweet']), axis=1)
df["Sentiment Score"] = df.apply(lambda x: sentiment_analyzer_scores(x['Tweet_English']), axis=1)


