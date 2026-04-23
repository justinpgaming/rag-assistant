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
You are a teaching assistant helping a beginner understand THEIR OWN code.

The following is the ACTUAL codebase:

{context}

USER QUESTION:
{user_query}

PROCESS (MANDATORY):

1. Search the provided code for the answer
2. If the function or item is NOT found:

Respond EXACTLY like this:

<item_name> → not found in provided code (may exist in another file)

3. If found:
→ explain using only the code

RULES:
- DO NOT assume location (no "above", "below", etc.)
- DO NOT invent missing code
- Only report what is visible
"""


def teach_mode(user_query, file_paths, llm_call):
    context = load_files(file_paths)
    prompt = build_prompt(user_query, context)

    return llm_call(prompt)
