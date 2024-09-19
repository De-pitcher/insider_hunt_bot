# src/monitor_follow_activity.py
import time
import json
import logging
from src.auth import authenticate_twitter
from src.notifications import send_dm
from config.config import TARGET_USER_ID

API = authenticate_twitter()


def check_rate_limits(api):
    rate_limits = api.rate_limit_status()
    return rate_limits["resources"]["statuses"]["/statuses/user_timeline"]


def wait_until_reset(reset_time):
    wait_seconds = reset_time - time.time()
    if wait_seconds > 0:
        print(f"Waiting for {wait_seconds} seconds until reset...")
        time.sleep(wait_seconds)


def load_json(filepath):
    try:
        with open(filepath, "r") as f:
            return set(json.load(f))
    except FileNotFoundError:
        return set()


def save_json(data, filepath):
    with open(filepath, "w") as f:
        json.dump(list(data), f)


def monitor_follow_activity():
    followers_file = "data/followers.json"
    following_file = "data/following.json"

    previous_followers = load_json(followers_file)
    previous_following = load_json(following_file)

    while True:
        try:
            limits = check_rate_limits(API)
            if limits["remaining"] <= 0:
                wait_until_reset(limits["reset"])
                
            current_followers = set(API.get_follower_ids(user_id=TARGET_USER_ID))
            current_following = set(API.get_friend_ids(user_id=TARGET_USER_ID))

            # New Followers
            new_followers = current_followers - previous_followers
            for follower_id in new_followers:
                user = API.get_user(user_id=follower_id)
                message = f"New follower: @{user.screen_name} has started following {TARGET_USER_ID}."
                send_dm(user_id=TARGET_USER_ID, text=message)
                logging.info(message)
                # Trigger notification here

            # New Following
            new_following = current_following - previous_following
            for follow_id in new_following:
                user = API.get_user(user_id=follow_id)
                logging.info(f"Started following: {user.screen_name}")
                # Trigger notification here

            # Unfollows
            unfollows = previous_following - current_following
            for unfollow_id in unfollows:
                user = API.get_user(user_id=unfollow_id)
                message = f"New unfollow: @{user.screen_name} has started unfollowed {TARGET_USER_ID}."
                send_dm(user_id=TARGET_USER_ID, text=message)
                logging.info(message)
                # Trigger notification here

            # Update stored data
            previous_followers = current_followers
            previous_following = current_following
            save_json(current_followers, followers_file)
            save_json(current_following, following_file)

        except Exception as e:
            logging.error(f"Error in monitor_follow_activity: {e}")

        time.sleep(60)  # Wait for 1 minute before next check
