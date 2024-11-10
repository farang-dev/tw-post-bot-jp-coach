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

def get_grammar_explanation():
    prompt = "You are a Japanese language teacher who simplifies grammar for English-speaking learners. Write a tweet explaining a common Japanese grammar point in easy-to-understand English(from n5 to n1 level - sometimes introduce a very advanced grammar). Include a short example sentence if possible. Limit the explanation to 280 characters.dont use a quotation mark."
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": prompt}]
    )
    return response['choices'][0]['message']['content'].strip()

def get_vocab_list():
    # Step 1: Ask OpenAI to suggest a theme for vocabulary
    theme_prompt = "Suggest a theme for a list of Japanese vocabulary words that would be interesting for English speakers learning Japanese. The theme should be completely randomized from the beginners to very advanced level(sometimes it also introduces very advanced vocaburary). dont use a quotation mark."
    theme_response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": theme_prompt}]
    )
    theme = theme_response['choices'][0]['message']['content'].strip()

    # Step 2: Generate vocabulary list based on the suggested theme
    vocab_prompt = f"As a Japanese vocabulary coach, create a tweet listing 5-10 Japanese vocabulary words related to the theme '{theme}' with short, simple English definitions. Randomize the content from the beginners to advanced level. at the end put hashtags(japanese learning related) that would generate the most impressions on X. Keep the tweet within 280 characters.dont use a quotation mark."
    vocab_response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": vocab_prompt}]
    )
    return vocab_response['choices'][0]['message']['content'].strip()


# List of content generation functions
content_generators = [
    get_grammar_explanation,
    get_vocab_list
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
