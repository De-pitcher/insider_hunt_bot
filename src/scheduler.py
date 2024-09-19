# src/scheduler.py
import threading
import logging
from src.monitor_follow_activity import monitor_follow_activity
from src.track_engagements import track_engagements
from src.monitor_new_memes_coin import monitor_new_memes_coin_accounts


def start_bot():
    try:
        threads = []

        # Thread for monitoring follow activity
        t1 = threading.Thread(target=monitor_follow_activity, daemon=True)
        threads.append(t1)
        t1.start()

        # Thread for tracking engagements
        t2 = threading.Thread(target=track_engagements, daemon=True)
        threads.append(t2)
        t2.start()

        # Thread for monitoring new meme coin accounts
        t3 = threading.Thread(target=monitor_new_memes_coin_accounts, daemon=True)
        threads.append(t3)
        t3.start()

        for t in threads:
            t.join()

    except KeyboardInterrupt:
        logging.info("Bot stopped by user.")
    except Exception as e:
        logging.error(f"Error in start_bot: {e}")
