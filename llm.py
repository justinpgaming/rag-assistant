import requests

def generate_answer(query, chunks):
    context = "\n\n".join([c["content"] for c in chunks])

    prompt = f"""
You are a precise and authoritative AI assistant.

The user is technically skilled (plumbing, gasfitting, refrigeration).
Respond in a clear, confident, and professional manner.

Instructions:
- Use the provided context as your primary source
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
                "stream": False
            }
        )
        return response.json().get("response", "")

    except Exception as e:
        return f"Error: {e}"
