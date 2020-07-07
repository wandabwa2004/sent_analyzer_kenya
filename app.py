import plotly.express as px
import streamlit as st
import twitter_utils
import pandas as pd
from PIL import Image
from bokeh.models.widgets import Div
import nltk 
nltk.download('stopwords')


image = Image.open('political_sentiments.png')


st.title('Kenyan Political Sentiments - The Polimeter ')
st.write('We carried out the analysis of sentiments of tweets disseminated by five political leaders  in Kenya. Emotions  in their tweets  were  mapped on the sentiments.')
st.subheader('What is sentiment analysis? ')
st.write ('Sentiment analysis is the mining of context in text and in the process identifying  subjective information related to the entity of interest.  Entities can be brands, products or services.')

st.write('Any positivity or negativity in the politicians  sentiments. We got the  last 3200 tweets from their timelines.')
st.image(image, caption='Positive  vs  Negative Tweets', use_column_width=True)
st.write("")
st.write("")
st.write(" The most positive sentiment is  1 and most negative is -1. Neutral tweets have a sentiment score of 0.")

authors = twitter_utils.authors
colors = twitter_utils.colors

freq_dict = {'Hour': 'H', 'Day': 'D', 'Week': 'W-Mon', 'Month': 'M', 'Year': 'Y'}

option = st.sidebar.selectbox('Choose the time durations for  the analysis',
                      ('Month', 'Week','Hour','Day'))
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
st.sidebar.markdown("Tip: Click on your  favourite  politician just once.")
st.sidebar.markdown("In addition, in the temporary charts you can select the period that interests you. If you double click on it you return to the original time window")

#st.write('Has seleccionado:', option)

live_tweeter = False

if live_tweeter:
    df = twitter_utils.getting_tweets(authors, n_tweets, pages)
    df.to_csv('last_tweets.csv', mode='a', header=False)
else:
    df_sentiment = pd.read_csv("tweets_sentiment_score.csv")
    df_emotions = pd.read_csv("tweets_emotions_score.csv")
    



freq_choosen = freq_dict[option]
df_sentiment_freq = twitter_utils.resample_df(df_sentiment, freq_choosen)
df_emotions_freq = twitter_utils.resample_df(df_emotions, freq_choosen)

fig = px.line(df_sentiment_freq, x='Date', y='Sentiment Score', color='Author', title="Temporal Evolution of Sentiment ",
              color_discrete_map=colors)
st.write(fig)

fig = px.box(df_sentiment, y="Sentiment Score", color="Author", title="Sentiment Rank",
             color_discrete_map=colors)
#st.write(fig)


st.write("Emotion in the Politician Tweets")

emotion = st.selectbox(' Choose the  emotion to analse',
                      ('anger', 'anticipation', 'disgust', 'fear', 'joy', 'negative', 'positive', 'sadness', 'surprise', 'trust'))

emotions = ['anger', 'anticipation', 'disgust', 'fear', 'joy', 'negative', 'positive', 'sadness', 'surprise', 'trust']

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
#st.write(fig)


st.write("A comparison of Emotions against different politicians.")
politicians = st.multiselect(label='Choose any two or  more politicians for  a side by side comparison',
                      options=authors, default=['WilliamsRuto', 'RailaOdinga'])

politicians_df_list = []

for x in politicians:
    df_unique_pol = df_unpivot[df_unpivot["Author"] == x]
    politicians_df_list.append(df_unique_pol)
politicians_df = pd.concat(politicians_df_list)


fig = px.bar(politicians_df, x="Emotions", y="Score", color="Author",barmode='group',color_discrete_map=colors)
fig.update_layout(autosize=True, showlegend=True, legend_orientation="h")
fig.update_yaxes(visible=True, showticklabels=True)
fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
st.write(fig)

st.write("")
st.write("Are you impressed by the sentiment and emotions of your favourite politician? Ultimately, they define them. Vote wisely.")

st.write("Number of  tweets in the analysis for the  politician.")
st.write(df_sentiment["Author"].value_counts())




if st.button('Interested in my career profile?)':
    js = "window.open('https://www.linkedin.com/in/wandabwaherman/')"  # New tab or window
    html = '<img src onerror="{}">'.format(js)
    div = Div(text=html)
    st.bokeh_chart(div)

if st.button('I sometimes blog..'):
    js = "window.open('https://medium.com/@hermanwandabwa')"  # New tab or window
    html = '<img src onerror="{}">'.format(js)
    div = Div(text=html)
    st.bokeh_chart(div)
    
# if st.button('Y si te apetece echarle un vistazo al código. Bienvenido!'):
#     js = "window.open('https://github.com/camorales197/tweets_sentiments')"  # New tab or window
#     html = '<img src onerror="{}">'.format(js)
#     div = Div(text=html)
#     st.bokeh_chart(div)


