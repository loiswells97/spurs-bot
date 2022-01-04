from textblob import TextBlob
import math
import tweepy

# from config import api

emojis = ["😩", "😭", "😢", "😟", "☺️", "😃", "🎉", "😱"]

def get_sentiment():

    tweets = tweepy.Cursor(api.search, q="#COYS").items(100)

    polarity = 0

    for tweet in tweets:
        analysis = TextBlob(tweet.text)
        # score = SentimentIntensityAnalyzer().polarity_scores(tweet.text)
        polarity += analysis.sentiment.polarity

    return emojis[floor(4+polarity/25)]

def get_text_sentiment(text):
    analysis = TextBlob(text)
    # score = SentimentIntensityAnalyzer().polarity_scores(tweet.text)
    polarity = analysis.sentiment.polarity

    emoji_index=math.floor(4+polarity/0.25)
    if emoji_index==8:
        emoji_index=7

    return emojis[emoji_index]
