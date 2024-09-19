# src/notifications.py
import tweepy
import logging
from config.config import API_KEY, API_SECRET_KEY, ACCESS_TOKEN, ACCESS_TOKEN_SECRET


# Authenticate Twitter API
def authenticate_twitter():
    auth = tweepy.OAuth1UserHandler(
        API_KEY, API_SECRET_KEY, ACCESS_TOKEN, ACCESS_TOKEN_SECRET
    )
    api = tweepy.API(auth, wait_on_rate_limit=True)
    return api


def send_dm(user_id, text):
    api = authenticate_twitter()
    try:
        api.send_direct_message(user_id=user_id, text=text)
        logging.info(f"DM sent to {user_id}: {text}")
    except Exception as e:
        logging.error(f"Failed to send DM to {user_id}: {e}")
