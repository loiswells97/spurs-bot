from textblob import TextBlob
import datetime
import math
import tweepy

from config import client

emojis = ["😩", "😭", "😢", "😟", "😊", "😃", "🎉", "😱"]

def get_sentiment():

    # tweets = tweepy.Cursor(api.search_tweets, q="#COYS").items(100)

    start_time = datetime.datetime.now()-datetime.timedelta(minutes=2)

    tweets = client.search_recent_tweets(query="#THFC", max_results=100, start_time=start_time)[0]

    polarity = 0

    for tweet in tweets:
        # print(tweet)
        analysis = TextBlob(tweet.text)
        # score = SentimentIntensityAnalyzer().polarity_scores(tweet.text)
        polarity += analysis.sentiment.polarity

    print(polarity/len(tweets))

    return emojis[math.floor(4+4*polarity/len(tweets))]

def get_text_sentiment(text):
    analysis = TextBlob(text)
    # score = SentimentIntensityAnalyzer().polarity_scores(tweet.text)
    polarity = analysis.sentiment.polarity

    emoji_index=math.floor(4+polarity/0.25)
    if emoji_index==8:
        emoji_index=7

    return emojis[emoji_index]
