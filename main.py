from fastapi import FastAPI
import json
from datetime import datetime, timezone
from pathlib import Path

from system_stats import get_system_stats

app = FastAPI()

LOG_FILE = Path("system_stats.log")


@app.get("/")
def read_root():
    return {"message": "Server Health Monitor API is running!"}


@app.get("/system")
def system_info():
    stats = get_system_stats()

    log_entry = {"timestamp": datetime.now(timezone.utc).isoformat(), "stats": stats}

    # Read the existing log entries
    try:
        with LOG_FILE.open("r") as log_file:
            log_data = json.load(log_file)
    except (FileNotFoundError, json.JSONDecodeError):
        log_data = []

    # Add the new entry to the existing log data
    log_data.append(log_entry)

    # Write the updated log back to the file
    with LOG_FILE.open("w") as log_file:
        json.dump(log_data, log_file, indent=4)

    print("System stats logged.")
    return stats
