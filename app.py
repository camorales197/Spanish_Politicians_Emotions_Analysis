import plotly.express as px
import streamlit as st
import twitter_utils
import pandas as pd
from PIL import Image
from bokeh.models.widgets import Div


image = Image.open('sentiment_table_example.png')


st.title('Análisis de Sentimiento para los Principales Políticos en Twitter')
st.write('En esta página hemos realizado un análisis de sentimiento a los últimos 3200 tweets de cada uno de los principales políticos en España con fecha de 15 de Junio de 2020.')
st.write('Antes de ponernos a mirar números, vamos a hacer una pequeña introducción al análisis de sentimiento. ',
         'El análisis de sentimiento es el proceso de determinar el tono emocional que hay detrás de una serie de palabras, y se utiliza para intentar entender las actitudes, opiniones y emociones expresadas.')

st.write(' Seguro que se entiende mejor viendo  los tweets mas positivos y los más negativos: ')
st.image(image, caption='Tweets más negativos y más positivos', use_column_width=True)
st.write("")
st.write("En la siguiente gráfica se muestran los resultados de clasificar cada tweet en una escala de muy positivo a muy negativo.")

authors = twitter_utils.authors
colors = twitter_utils.colors


freq_dict = {'Hora': 'H', 'Día': 'D', 'Semana': 'W-Mon', 'Mes': 'M', 'Año': 'Y'}

option = st.sidebar.selectbox('Para mejorar la visualización temporal, es necesario agrupar los tweets por fechas.'
                      ' ¿Como te gustaría hacerlo?',
                      ('Mes', 'Semana'))
st.sidebar.markdown("")
st.sidebar.markdown("")
st.sidebar.markdown("")
st.sidebar.markdown("")
st.sidebar.markdown("")
st.sidebar.markdown("")
st.sidebar.markdown("")
st.sidebar.markdown("")
st.sidebar.markdown("")
st.sidebar.markdown("")
st.sidebar.markdown("")
st.sidebar.markdown("Consejo: Si pinchas una vez sobre el nombre de un político en la leyenda, este sale del gráfico. "
                    "Si pinchas dos veces, se queda solo en el gráfico")

#st.write('Has seleccionado:', option)

live_tweeter = False

if live_tweeter:
    df = twitter_utils.getting_tweets(authors, n_tweets, pages)
    df.to_csv('last_tweets.csv', mode='a', header=False)
else:
    df_sentiment = pd.read_csv("tweets_sentiment_score.csv")
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

fig = px.line(df_emotions_freq, x="Date", y=emotion, color='Author',
                  title='{} Sentiment'.format(emotion.title()),
                 color_discrete_map=colors)
st.write(fig)


st.write("Por último veamos que políticos utilizan más cada emoción.")

df_pivot = df_emotions.groupby(by="Author").mean()
df_pivot = df_pivot.drop("word_count", axis=1)
df_pivot = df_pivot.reset_index()
df_unpivot = df_pivot.melt(id_vars=["Author"], var_name='Emotions', value_name='Score')
df_unpivot.sort_values(by="Score", inplace=True, ascending=False)

fig = px.bar(df_unpivot, x="Emotions", y="Score", color="Author", color_discrete_map=colors)
st.write(fig)

st.write("")
st.write("¿Que conclusiones sacas? " 
         "¿Se te ocurre algun otro análisis interesante? ")



#st.write("Número de tweets analizados por político.")
#st.write(df_sentiment["Author"].value_counts())




if st.button('Hablemos! :)'):
    js = "window.open('https://www.linkedin.com/in/carloscamorales')"  # New tab or window
    html = '<img src onerror="{}">'.format(js)
    div = Div(text=html)
    st.bokeh_chart(div)


if st.button('Y si te apetece echarle un vistazo al código. Bienvenido!'):
    js = "window.open('https://github.com/camorales197/tweets_sentiments')"  # New tab or window
    html = '<img src onerror="{}">'.format(js)
    div = Div(text=html)
    st.bokeh_chart(div)


