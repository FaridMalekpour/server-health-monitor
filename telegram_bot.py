import json
import os
import logging
from telegram import Bot

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
LOG_FILE = "system_stats.log"

bot = Bot(token=TOKEN)

def get_last_log():
    """ Reads the last log entry from the file """
    try:
        with open(LOG_FILE, "r") as file:
            logs = file.readlines()
            if not logs:
                return "No logs found."
            last_log = json.loads(logs[-1])  # Parse the last JSON object
            return f"📊 *System Status Update:*\n🕒 {last_log['timestamp']}\n\n```json\n{json.dumps(last_log['stats'], indent=2)}```"
    except Exception as e:
        logging.error(f"Error reading log file: {e}")
        return "⚠️ Error retrieving logs."

def send_latest_log():
    """ Sends the last log entry to the Telegram user """
    message = get_last_log()
    bot.send_message(chat_id=CHAT_ID, text=message, parse_mode="Markdown")

if __name__ == "__main__":
    send_latest_log()

