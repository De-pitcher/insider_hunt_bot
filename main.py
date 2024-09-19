# main.py
import logging
from src.scheduler import start_bot  # or start_scheduler


def main():
    logging.info("Starting Twitter Bot...")
    start_bot()  # Starts all monitoring threads


if __name__ == "__main__":
    main()
