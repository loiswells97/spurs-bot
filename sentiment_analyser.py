from textblob import TextBlob
import datetime
import math
import tweepy

from config import client

emojis = ["😩", "😭", "😢", "😟", "😊", "😃", "🎉", "😱"]

def get_sentiment():

    start_time = datetime.datetime.now()-datetime.timedelta(seconds=30)

    tweets = client.search_recent_tweets(query="#COYS", max_results=100, start_time=start_time)[0]

    polarity = 0
    if tweets is not None:
        for tweet in tweets:
            analysis = TextBlob(tweet.text)
            polarity += analysis.sentiment.polarity

        mean_polarity=polarity/len(tweets)
    else:
        mean_polarity=0

    print(mean_polarity)

    return emojis[math.floor(4+4*mean_polarity)]

def get_text_sentiment(text):
    analysis = TextBlob(text)
    polarity = analysis.sentiment.polarity

    emoji_index=math.floor(4+polarity/0.25)
    if emoji_index==8:
        emoji_index=7

    return emojis[emoji_index]
