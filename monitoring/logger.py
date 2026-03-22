import json
from datetime import datetime

LOG_FILE = "monitoring/storage.json"

def log_event(data):
    entry = {
        "timestamp": str(datetime.now()),
        **data
    }

    try:
        with open(LOG_FILE, "r") as f:
            logs = json.load(f)
    except:
        logs = []

    logs.append(entry)

    with open(LOG_FILE, "w") as f:
        json.dump(logs, f, indent=2)