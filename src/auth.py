import logging
import tweepy

from config.config import API_KEY, API_SECRET_KEY, ACCESS_TOKEN, ACCESS_TOKEN_SECRET


def authenticate_twitter():
    try:
        auth = tweepy.OAuth1UserHandler(
            API_KEY, API_SECRET_KEY, ACCESS_TOKEN, ACCESS_TOKEN_SECRET
        )
        api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
        api.verify_credentials()
        logging.info("Authentication Successful")
        return api
    except Exception as e:
        logging.error(f"Error during authentication: {e}")
        raise e
