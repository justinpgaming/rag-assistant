import json

LOG_FILE = "logs.jsonl"


def view_logs(n=5):
    try:
        with open(LOG_FILE, "r") as f:
            lines = f.readlines()

        if not lines:
            print("⚠ No logs found")
            return

        # Get last n entries
        entries = lines[-n:]

        for i, line in enumerate(entries, 1):
            log = json.loads(line)

            print("\n" + "=" * 50)
            print(f"🧾 Log Entry {i}")
            print("=" * 50)

            print(f"🕒 Time: {log.get('timestamp', 'N/A')}")
            print(f"❓ Query: {log.get('query', 'N/A')}")

            print("\n📦 Chunks:")
            for c in log.get("chunks", []):
                preview = c[:100].replace("\n", " ")
                print(f"- {preview}...")

            print("\n🧠 Prompt:")
            print(log.get("prompt", "")[:500] + "...")

            print("\n🤖 Response:")
            print(log.get("response", ""))

        print("\n✅ End of logs\n")

    except FileNotFoundError:
        print("⚠ Log file not found")
    except Exception as e:
        print(f"⚠ Error reading logs: {e}")
