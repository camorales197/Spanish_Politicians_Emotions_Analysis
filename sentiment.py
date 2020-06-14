import twitter_utils
import plotly.express as px
import streamlit as st


def truncate_date(input_date):
    return input_date.date()


st.title('Análisis de Sentimiento en Twitter')

authors = ['sanchezcastejon', 'pablocasado_', 'PabloIglesias', 'Santi_ABASCAL', 'InesArrimadas']
n_tweets = 2

df = twitter_utils.getting_tweets(authors, n_tweets)

df['Date'] = df.apply(lambda x: truncate_date(x['Date']),axis=1)

df_group = df.groupby(['Date', 'Author']).mean()
df_group.reset_index(inplace=True)

fig = px.line(df_group, x='Date', y='Score', color='Author', title="Análisis Temporal de Sentimiento Políticos España")
fig.show()

fig = px.box(df, y="Score", color="Author", title="Análisis de Sentimiento Políticos España")
fig.show()