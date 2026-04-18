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
        return data.get("response", "")

    except Exception as e:
        return f"\nError: {e}\n"


