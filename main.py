from fastapi import FastAPI
import json
from datetime import datetime, timezone
from pathlib import Path
import os

from system_stats import get_system_stats

app = FastAPI()

LOG_FILE = Path("system_stats.log")


@app.get("/")
def read_root():
    return {"message": "Server Health Monitor API is running!"}


@app.get("/system")
def system_info():
    stats = get_system_stats()
    log_entry = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "stats": stats,
    }

    # Check if file exists and contains valid JSON
    if os.path.exists(LOG_FILE) and os.path.getsize(LOG_FILE) > 0:
        try:
            with open(LOG_FILE, "r") as log_file:
                logs = json.load(log_file)
                if not isinstance(logs, list):
                    logs = []  # If it's not a list, reset it
        except json.JSONDecodeError:
            logs = []  # If invalid JSON, reset it
    else:
        logs = []

    # Append new entry and write back as a valid JSON array
    logs.append(log_entry)
    with open(LOG_FILE, "w") as log_file:
        json.dump(logs, log_file, indent=4)

    print("System stats logged.")
    return stats
