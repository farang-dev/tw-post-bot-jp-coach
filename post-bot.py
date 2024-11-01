import openai
import tweepy
import os
import random
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

# Define each type of prompt for the six content types
def get_learning_advice():
    prompt = "You are a Japanese language coach providing advice for English speakers learning Japanese. Create a tweet in English that gives a motivational tip or practical learning strategy for studying Japanese. Keep it simple and encouraging for beginners to intermediate learners. Limit to 280 characters. dont use a quotation mark."
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": prompt}]
    )
    return response['choices'][0]['message']['content'].strip()

def get_grammar_explanation():
    prompt = "You are a Japanese language teacher who simplifies grammar for English-speaking learners. Write a tweet explaining a common Japanese grammar point in easy-to-understand English. Include a short example sentence if possible. Limit the explanation to 280 characters.dont use a quotation mark."
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": prompt}]
    )
    return response['choices'][0]['message']['content'].strip()

def get_vocab_list():
    # Step 1: Ask OpenAI to suggest a theme for vocabulary
    theme_prompt = "Suggest a theme for a list of Japanese vocabulary words that would be interesting for English speakers learning Japanese. The theme should be simple and common, like 'food' or 'travel'.dont use a quotation mark."
    theme_response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": theme_prompt}]
    )
    theme = theme_response['choices'][0]['message']['content'].strip()

    # Step 2: Generate vocabulary list based on the suggested theme
    vocab_prompt = f"As a Japanese vocabulary coach, create a tweet listing 5-10 Japanese vocabulary words related to the theme '{theme}' with short, simple English definitions. Make it easy for beginners, and keep the tweet within 280 characters.dont use a quotation mark."
    vocab_response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": vocab_prompt}]
    )
    return vocab_response['choices'][0]['message']['content'].strip()

def get_daily_phrase():
    prompt = "You are a Japanese language coach providing useful phrases for daily conversation. Write a tweet introducing a helpful Japanese phrase or expression, explaining its meaning and providing a simple example in English. Keep it within 280 characters."
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": prompt}]
    )
    return response['choices'][0]['message']['content'].strip()

def get_synonym_thesaurus():
    prompt = "As a Japanese language coach, create a tweet introducing a common Japanese word, along with 3-5 synonyms or related words and brief explanations in English. Keep it friendly and within 280 characters.dont use a quotation mark."
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": prompt}]
    )
    return response['choices'][0]['message']['content'].strip()

def get_pronunciation_tip():
    prompt = "You are a pronunciation expert. Write a tweet that provides an easy tip to help English speakers improve their pronunciation of a common but challenging Japanese word. Include phonetic hints or a short practice tip. Keep it within 280 characters.dont use a quotation mark."
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": prompt}]
    )
    return response['choices'][0]['message']['content'].strip()

# List of content generation functions
content_generators = [
    get_learning_advice,
    get_grammar_explanation,
    get_vocab_list,
    get_daily_phrase,
    get_synonym_thesaurus,
    get_pronunciation_tip
]

def tweet_content():
    """Tweet randomly selected content."""
    try:
        # Select a random content generator
        content_func = random.choice(content_generators)
        content = content_func()

        # Post the tweet
        response = client.create_tweet(text=content)
        tweet_id = response.data['id']
        print(f"Tweeted: {content} (Tweet ID: {tweet_id})")
    except tweepy.TooManyRequests as e:
        print("Rate limit reached. Exiting script...")
    except Exception as e:
        print(f"Error tweeting: {e}")

if __name__ == "__main__":
    tweet_content()  # Run the content generation and tweeting once
