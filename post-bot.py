import openai
import tweepy
import os
import random
import time
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# OpenAI API setup
openai.api_key = os.getenv("OPENAI_API_KEY")

# Twitter API v2 setup using Client
client = tweepy.Client(
    consumer_key=os.getenv("CONSUMER_KEY"),
    consumer_secret=os.getenv("CONSUMER_SECRET"),
    access_token=os.getenv("ACCESS_TOKEN"),
    access_token_secret=os.getenv("ACCESS_TOKEN_SECRET")
)

def get_news_articles():
    """Fetch news articles from RSS feeds"""
    import feedparser
    from datetime import datetime, timedelta

    # List of RSS feeds from reputable English news sources
    rss_feeds = [
        "http://feeds.bbci.co.uk/news/world/rss.xml",
        "https://www.reutersagency.com/feed/?taxonomy=best-topics&post_type=best",
        "https://www.theguardian.com/world/rss",
        "https://www.nytimes.com/svc/collections/v1/publish/https://www.nytimes.com/section/world/rss.xml"
    ]

    articles = []
    for feed_url in rss_feeds:
        feed = feedparser.parse(feed_url)
        for entry in feed.entries:
            # Only include recent articles (last 24 hours)
            if datetime.now() - datetime(*entry.published_parsed[:6]) < timedelta(hours=24):
                articles.append({
                    'title': entry.title,
                    'description': entry.summary,
                    'source': {'name': feed.feed.title}
                })
                if len(articles) >= 5:  # Limit to 5 articles
                    return articles
    return articles

def translate_to_japanese(text):
    """Translate English text to Japanese using OpenAI"""
    from openai import OpenAI
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    prompt = f"Translate this news article into Japanese, making it concise and suitable for a tweet (max 280 characters):\n\n{text}\n\nProvide only the Japanese translation without any additional text or explanations."
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": prompt}]
    )
    return response.choices[0].message.content.strip()

def generate_news_tweet():
    """Generate a tweet from news articles"""
    articles = get_news_articles()
    if not articles:
        return None

    # Select a random article
    article = random.choice(articles)
    title = article['title']
    description = article['description'] or title

    # Translate to Japanese
    japanese_text = translate_to_japanese(description)

    # Add source attribution if space allows
    if len(japanese_text) < 250 and article['source']['name']:
        japanese_text += f"\n\n(Source: {article['source']['name']})"

    return japanese_text

def tweet_content():
    """Tweet news content continuously"""
    while True:
        try:
            content = generate_news_tweet()
            if content:
                response = client.create_tweet(text=content)
                tweet_id = response.data['id']
                print(f"Tweeted: {content} (Tweet ID: {tweet_id})")
            else:
                print("No news articles found")

            # Wait for 1 hour before next tweet
            time.sleep(3600)

        except tweepy.TooManyRequests as e:
            print("Rate limit reached. Waiting 15 minutes...")
            time.sleep(900)
        except Exception as e:
            print(f"Error tweeting: {e}")
            time.sleep(600)

if __name__ == "__main__":
    tweet_content()  # Run the news broadcasting bot
