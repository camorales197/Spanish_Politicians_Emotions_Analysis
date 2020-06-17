import plotly.express as px
import streamlit as st
import twitter_utils
import pandas as pd


st.title('Análisis de Sentimiento para los Principales Políticos en Twitter')
st.write('En esta página se pueden ver los resultados de un análisis de sentimiento realizado sobre los últimos tweets de los principales políticos españoles.')
st.write('Antes de ponernos a mirar números, vamos a hacer una pequeña introducción al análisis de sentimiento. ',
         'El análisis de sentimiento, también conocido como minería de opinión (opinion mining), es un término muy discutido pero a menudo incomprendido. Básicamente, es el proceso de determinar el tono emocional que hay detrás de una serie de palabras, y se utiliza para intentar entender las actitudes, opiniones y emociones expresadas.')
st.write('Se pueden realizar diferentes tipos de análisis. En esta página hemos realizado los suigientes:'
         '  - Analisis de Sentimiento que mide el uso de un leng y BLaBLaBLA')

st.write('Primero un análisis sencillo de sentimiento. '
         'Cada tweet se clasifica de -1 (Muy negativo) a +1 (Muy positivo) pasando por 0 (Neutro).')
st.write("")
st.write("")

authors = twitter_utils.authors
colors = twitter_utils.colors


freq_dict = {'Hora': 'H', 'Día': 'D', 'Semana': 'W-Mon', 'Mes': 'M', 'Año': 'Y'}

option = st.selectbox('Para mejorar la visualización temporal, es necesario agrupar los tweets por fechas.'
                      ' ¿Como te gustaría hacerlo?',
                      ('Mes', 'Semana', 'Día'))

st.write('Has seleccionado:', option)

live_tweeter = False

if live_tweeter:
    df = twitter_utils.getting_tweets(authors, n_tweets, pages)
    df.to_csv('last_tweets.csv', mode='a', header=False)
else:
    df_sentiment = pd.read_csv("tweets_sentiment_score.csv")
    df_sentiment = df_sentiment[df_sentiment.Author != 'gabrielrufian']
    df_emotions = pd.read_csv("tweets_emotions_score.csv")
    df_emotions = df_emotions[df_emotions.Author != 'gabrielrufian']



freq_choosen = freq_dict[option]
df_sentiment_freq = twitter_utils.resample_df(df_sentiment, freq_choosen)
df_emotions_freq = twitter_utils.resample_df(df_emotions, freq_choosen)

fig = px.line(df_sentiment_freq, x='Date', y='Sentiment Score', color='Author', title="Evolución Temporal de Sentimientos por Político",
              color_discrete_map=colors)
st.write(fig)

fig = px.box(df_sentiment, y="Sentiment Score", color="Author", title="Rango de Sentimiento por Político",
             color_discrete_map=colors)
#st.write(fig)


st.write("Tambien se pueden analizar las emociones por separado.")
emotion = st.selectbox(' ¿Que emoción te gustaría analizar?',
                      ('anger', 'anticipation', 'disgust', 'fear', 'joy', 'negative', 'positive', 'sadness', 'surprise', 'trust'))

emotions = ['anger', 'anticipation', 'disgust', 'fear', 'joy', 'negative', 'positive', 'sadness', 'surprise', 'trust']

st.write("Veamos que emociones son más utilizadas por cada político")
fig = px.line(df_emotions_freq, x="Date", y=emotion, color='Author',
                  title='{} Sentiment'.format(emotion.title()),
                 color_discrete_map=colors)
st.write(fig)


df_pivot = df_emotions.groupby(by="Author").mean()
df_pivot = df_pivot.drop("word_count", axis=1)
df_pivot = df_pivot.reset_index()
df_unpivot = df_pivot.melt(id_vars=["Author"], var_name='Emotions', value_name='Score')
df_unpivot.sort_values(by="Score", inplace=True, ascending=False)

fig = px.bar(df_unpivot, x="Emotions", y="Score", color="Author", color_discrete_map=colors)
st.write(fig)


st.write("Número de tweets analizados por político.")
#st.write(df_sentiment["Author"].value_counts())
