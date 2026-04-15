import requests
import json

def generate_answer(query, chunks, memory):
    context = "\n\n".join([c["content"] for c in chunks])

    goals = "\n".join(f"- {g}" for g in memory.get("goals", []))
    decisions = "\n".join(f"- {d}" for d in memory.get("decisions", []))

    prompt = f"""
You are a precise and authoritative AI assistant.

The user is technically skilled (plumbing, gasfitting, refrigeration).
Respond in a clear, confident, and professional manner.

User Goals:
{goals if goals else "None"}

Key Decisions:
{decisions if decisions else "None"}

Instructions:
- Use the provided context as your primary source
- Align answers with user goals when relevant
- Respect prior decisions if applicable
- Do NOT make up information
- If unsure, say "I don't know"
- Keep answers concise and structured
- Prefer bullet points when helpful
- Avoid unnecessary words or repetition
- Be confident and direct in your explanations
- You may include small amounts of general knowledge ONLY if it supports or clarifies the context
- Do NOT introduce unrelated or overly niche details

Context:
{context}

Question:
{query}

Answer (concise, clear, authoritative):
"""

    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3",
                "prompt": prompt,
                "stream": True
            },
            stream=True
        )

        for line in response.iter_lines():
            if line:
                data = json.loads(line.decode("utf-8"))
                if "response" in data:
                    yield data["response"]

    except Exception as e:
        yield f"\nError: {e}\n"
