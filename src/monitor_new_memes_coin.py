# src/monitor_new_memes_coin.py
import json
import time
import logging
from datetime import datetime, timedelta
from src.auth import authenticate_twitter

API = authenticate_twitter()


def monitor_new_memes_coin_accounts():
    tracked_accounts_file = "data/new_memes_coin_accounts.json"
    try:
        with open(tracked_accounts_file, "r") as f:
            tracked_accounts = set(json.load(f))
    except FileNotFoundError:
        tracked_accounts = set()

    query = "memes coin OR $meme"
    search_count = 20  # Number of accounts to fetch each time

    while True:
        try:
            # Twitter API v2 might have better search capabilities; adjust accordingly
            new_accounts = API.search_users(q=query, count=search_count)

            for account in new_accounts:
                if account.id in tracked_accounts:
                    continue  # Already tracked

                account_creation_time = account.created_at
                if account_creation_time and (
                    datetime.utcnow() - account_creation_time.replace(tzinfo=None)
                ) < timedelta(hours=24):
                    logging.info(
                        f"New Meme Coin Account Detected: {account.screen_name}, Created at {account_creation_time}"
                    )
                    # Trigger notification here
                    tracked_accounts.add(account.id)

            # Save updated tracked accounts
            with open(tracked_accounts_file, "w") as f:
                json.dump(list(tracked_accounts), f)

        except Exception as e:
            logging.error(f"Error in monitor_new_memes_coin_accounts: {e}")

        time.sleep(600)  # Wait for 10 minutes before next check
