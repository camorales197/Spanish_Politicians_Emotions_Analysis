import pandas as pd
from nltk.stem.snowball import SnowballStemmer
from tqdm.notebook import tqdm
from nltk import word_tokenize
from nltk import tokenize
from nltk.corpus import stopwords


def text_emotion(df, column):
    '''
    Takes a DataFrame and a specified column of text and adds 10 columns to the
    DataFrame for each of the 10 emotions in the NRC Emotion Lexicon, with each
    column containing the value of the text in that emotions
    INPUT: DataFrame, string
    OUTPUT: the original DataFrame with ten new columns
    '''

    new_df = df.copy()

    emolex_df = pd.read_csv("NRC-Emotion-Lexicon-Wordlevel-v0.92.txt",
                            names=["word", "emotion", "association"],
                            sep='\t')
    emolex_words = emolex_df.pivot(index='word',
                                   columns='emotion',
                                   values='association').reset_index()
    emotions = emolex_words.columns.drop('word')
    emo_df = pd.DataFrame(0, index=df.index, columns=emotions)

    stemmer = SnowballStemmer("english")

    with tqdm(total=len(list(new_df.iterrows()))) as pbar:
        for i, row in new_df.iterrows():
            pbar.update(1)
            try:
                document = word_tokenize(new_df.loc[i][column])
                for word in document:
                    try:
                        word = stemmer.stem(word.lower())
                        emo_score = emolex_words[emolex_words.word == word]
                        if not emo_score.empty:
                            for emotion in list(emotions):
                                emo_df.at[i, emotion] += emo_score[emotion]
                    except:
                        print("Error at: ", row)
                        pass
            except:
                print("Error at: ", row)
                pass

    new_df = pd.concat([new_df, emo_df], axis=1)

    return new_df


def number_of_words(sentence):
    try:
        x = 0
        tok = tokenize.word_tokenize(sentence)
        for word in tok:
            if word in stop_words:
                x += 1
        return len(tok) - x
    except:
        return None
        pass

stop_words = set(stopwords.words('english'))

df = pd.read_csv("tweets_sentiment_score.csv", usecols=["Author", "Date", "Tweet_English"]
                 ,dtype={'Author': object, 'Date': object, 'Tweet_English': object})
#df = df[0:50]

df_emotions = text_emotion(df, "Tweet_English")

df_emotions['word_count'] = df.apply(lambda x: number_of_words(x['Tweet_English']), axis=1)

emotions = ['anger', 'anticipation', 'disgust', 'fear', 'joy', 'negative', 'positive', 'sadness', 'surprise', 'trust']

for emotion in emotions:
    df_emotions[emotion] = df_emotions[emotion] / df_emotions['word_count']

df_unique = df_emotions.drop_duplicates(['Date'])
df_unique = df_unique.drop_duplicates(['Tweet_English'])
df_unique = df_unique[df_unique.Author != 'gabrielrufian'] #todo delete it in the future
df_unique = df_unique.dropna(axis='index')

df_unique.to_csv('tweets_emotions_score.csv', index=False)
print(df_unique)
print("Cé finit!")


