import json
from datetime import datetime

LOG_FILE = "logs.jsonl"


def log_event(query, chunks, response, prompt):
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "query": query,
        "prompt": prompt,
        "chunks": [c["content"] for c in chunks],
        "response": response
    }

    try:
        with open(LOG_FILE, "a") as f:
            f.write(json.dumps(log_entry) + "\n")

        print("📝 Logged")

    except Exception as e:
        print(f"⚠ Logging error: {e}")
