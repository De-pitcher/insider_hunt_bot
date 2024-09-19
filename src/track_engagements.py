# src/track_engagements.py
import time
import json
import logging
from src.auth import authenticate_twitter
from config.config import TARGET_USER_ID

API = authenticate_twitter()

def load_last_seen(filepath):
    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_last_seen(data, filepath):
    with open(filepath, 'w') as f:
        json.dump(data, f)

def track_engagements():
    last_seen_file = 'data/last_seen_tweet.json'
    last_seen = load_last_seen(last_seen_file)
    
    while True:
        try:
            tweets = API.user_timeline(user_id=TARGET_USER_ID, since_id=last_seen.get('tweet_id'), count=10, tweet_mode='extended')
            for tweet in reversed(tweets):
                # Update last seen tweet ID
                if 'tweet_id' not in last_seen or tweet.id > last_seen['tweet_id']:
                    last_seen['tweet_id'] = tweet.id
                    save_last_seen(last_seen, last_seen_file)
                
                # Check engagements
                if tweet.favorite_count > 0:
                    logging.info(f"Tweet ID {tweet.id} was liked {tweet.favorite_count} times.")
                    # Trigger notification here
                if tweet.retweet_count > 0:
                    logging.info(f"Tweet ID {tweet.id} was retweeted {tweet.retweet_count} times.")
                    # Trigger notification here
                # Note: To track comments (replies), you'd need to use the search API or stream.
                
        except Exception as e:
            logging.error(f"Error in track_engagements: {e}")
        
        time.sleep(60)  # Wait for 1 minute before next check
