"""
FILE: teach_mode.py

PURPOSE:
Provide grounded explanations of code using strict context rules.

KEY RULE:
If something is not in provided code → it does not exist.

STATUS:
v1 working (grounded, no assumptions)
"""


def load_files(file_paths):
    contents = []

    for path in file_paths:
        try:
            with open(path, "r") as f:
                contents.append(f"\n--- FILE: {path} ---\n" + f.read())
        except:
            contents.append(f"\n--- FILE: {path} (FAILED TO LOAD) ---\n")

    return "\n".join(contents)


def build_prompt(user_query, context):
    return f"""
You are a STRICT code lookup tool.

You are ONLY allowed to check if something exists in the provided code.
Only explain what is explicitly present in the code.
Do not assume relationships between functions unless shown.
If something is unclear, say so.

---------------------
CODEBASE:
{context}
---------------------

USER QUERY:
{user_query}

TASK:

1. Extract the exact name being asked about.
2. Search for that EXACT name in the code.
3. Do NOT modify the name.
4. Do NOT guess similar names.

OUTPUT FORMAT (MANDATORY):

IF FOUND:
FOUND: <exact name>
DETAIL: <only what is visible in code>

IF NOT FOUND:
NOT_FOUND: <exact name>

RULES:

- ONLY output in this format
- NO extra text
- NO explanations
- NO assumptions
- NO mentioning external libraries
- NO mentioning "larger program"
- NO guessing
"""

import re


def extract_target(query: str) -> str:
    query = query.lower()

    patterns = [
        r"where is ([a-zA-Z_][a-zA-Z0-9_]*)",
        r"explain ([a-zA-Z_][a-zA-Z0-9_]*)",
        r"describe ([a-zA-Z_][a-zA-Z0-9_]*)",
        r"what is ([a-zA-Z_][a-zA-Z0-9_]*)",
    ]

    for pattern in patterns:
        match = re.search(pattern, query)
        if match:
            return match.group(1)

    return None


def teach_mode(user_query, file_paths, llm_call):
    context = load_files(file_paths)

    target = extract_target(user_query)
    print(f"DEBUG TARGET: [{target}]")

    # -----------------------------
    # HARD VALIDATION (existence)
    # -----------------------------
    if target and target not in context:
        return f"I did not find {target} in the provided code."

    # -----------------------------
    # LLM CALL
    # -----------------------------
    prompt = build_prompt(user_query, context)
    response = llm_call(prompt)

    # -----------------------------
    # LIGHT VALIDATION (guess detection)
    # -----------------------------
    mentions = re.findall(r"\b[a-zA-Z_][a-zA-Z0-9_]*\b", response)
    unknown = [m for m in mentions if m not in context]

    if unknown:
        print(f"⚠️ POSSIBLE GUESSING: {unknown}")

    # -----------------------------
    # OUTPUT GUARD
    # -----------------------------
    response = guard_teach_output(response, context)

    return response


def guard_teach_output(response: str, context: str) -> str:
    banned_phrases = [
        "seems",
        "appears",
        "likely",
        "probably",
        "part of a larger",
        "not shown here",
        "based on typical",
        "in general",
    ]

    banned_keywords = ["tensorflow", "numpy", "pytorch", "fast mode"]

    response_lower = response.lower()
    context_lower = context.lower()

    # -----------------------------
    # Speculation guard
    # -----------------------------
    for phrase in banned_phrases:
        if phrase in response_lower:
            return "❌ Ungrounded response blocked (speculation detected)"

    # -----------------------------
    # Context leak guard
    # -----------------------------
    for word in banned_keywords:
        if word in response_lower and word not in context_lower:
            return f"❌ Ungrounded response blocked (invalid reference: {word})"

    return response
