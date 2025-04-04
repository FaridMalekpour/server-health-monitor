import json
import os
import logging
from telegram import Bot
import asyncio

# Load environment variables
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
LOG_FILE = "system_stats.log"

bot = Bot(token=TOKEN)


def get_last_log():
    """Reads the last log entry from the file"""
    try:
        with open(LOG_FILE, "r") as file:
            logs = json.load(file)  # Load entire JSON array
            if not logs:
                return "No logs found."

            last_log = logs[-1]  # Get last entry
            stats = last_log["stats"]  # Fix incorrect key

            main_string = f"📊 System Status Update:\n🕒 {last_log['timestamp']}\n\n"

            for key, value in stats.items():  # Fix iteration
                main_string += f"🔹 {key.capitalize()}\n"
                for k, v in value.items():
                    if isinstance(v, dict) and "value" in v and "unit" in v:
                        main_string += f"  - {k}: {v['value']} {v['unit']}\n"
                    else:
                        main_string += f"  - {k}: {v}\n"  # Handle plain integers
                main_string += "\n"
            return main_string
    except json.JSONDecodeError:
        logging.error("Log file contains invalid JSON.")
        return "⚠️ Log file contains invalid JSON."
    except Exception as e:
        logging.error(f"Error reading log file: {e}")
        return "⚠️ Error retrieving logs."


async def send_latest_log():
    """Sends the last log entry to the Telegram user"""
    message = get_last_log()
    await bot.send_message(chat_id=CHAT_ID, text=message)


if __name__ == "__main__":
    asyncio.run(send_latest_log())
