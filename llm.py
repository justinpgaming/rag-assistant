import requests
import json

def generate_answer(prompt):
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3",
                "prompt": prompt,
                "stream": False
            }
        )

        data = response.json()
        yield data.get("response", "")

    except Exception as e:
        yield f"\nError: {e}\n"
