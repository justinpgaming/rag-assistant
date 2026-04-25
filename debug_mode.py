# debug_mode.py


def extract_code_block(user_input: str):
    """
    Extracts code blocks from user input.
    Looks for [FILE: ...] pattern.
    """

    if "[FILE:" not in user_input:
        return None

    try:
        start = user_input.index("[FILE:")
        end = user_input.index("]", start)
        header = user_input[start : end + 1]

        code = user_input[end + 1 :].strip()

        return header, code
    except:
        return None


def run_debug_mode(user_input: str, llm_call_fn):
    print("DEBUG MODE ACTIVATED")

    """
    Debug Mode:
    Helps debug user code or system behavior.
    """

    # -----------------------------
    # ERROR PARSING (FIXED INDENT)
    # -----------------------------
    if "[ERROR]" in user_input:
        prompt = f"""
You are a debugging assistant helping fix a Python system.

The user encountered an error.

{user_input}

Your job:
1. Identify EXACT cause of the error
2. Explain WHY it happens (in simple terms)
3. Show EXACT fix
4. Specify FILE and LINE where fix goes
5. Show corrected code block

Rules:
- Be precise
- No guessing
- No vague advice
"""
        return llm_call_fn(prompt)

    # -----------------------------
    # CODE BLOCK HANDLING
    # -----------------------------
    extracted = extract_code_block(user_input)

    if extracted:
        header, code = extracted

        prompt = f"""
You are a debugging assistant helping a beginner.

The user provided code.

{header}

CODE:
{code}

Your job:
1. Identify ALL issues
2. Explain WHY each issue happens
3. Provide EXACT fixes
4. Show FULL corrected code
5. Specify EXACT placement if partial fix

Rules:
- The provided code is the SOURCE OF TRUTH. Do NOT invent missing structures.
- No vague advice
- No assumptions
- No skipping steps
- Keep explanations clear and simple
"""
    else:
        # -----------------------------
        # GENERAL DEBUG
        # -----------------------------
        prompt = f"""
You are a debugging assistant helping fix a Python system.

The user encountered an error.

INPUT:
{user_input}

Your job:
1. Identify the EXACT cause of the error
2. Explain WHY it happens (in simple terms)
3. Show the EXACT fix
4. Use the PROVIDED file name if present
5. If no file is provided, say "FILE UNKNOWN"
6. DO NOT invent file names or line numbers
7. Show corrected code block ONLY if confident

Rules:
- Be precise
- No guessing
- No vague advice
- If missing information, clearly state what is missing
"""

    # -----------------------------
    # FINAL CALL
    # -----------------------------
    response = llm_call_fn(prompt)

    return response if response else "DEBUG: EMPTY RESPONSE"
