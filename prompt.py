# =========================================
# 🧠 Prompt Builder (Mode-Aware)
# =========================================

def build_prompt(query, context, mode):
    mode_map = {
        "fast": FAST_PROMPT,
        "think": THINK_PROMPT,
        "tool": TOOL_PROMPT
    }

    mode_instruction = mode_map.get(mode, "")

    if mode == "tool":
        base = f"""
User Query:
{query}
"""
    else:
        base = f"""
Context:
{context}

User Query:
{query}

Instructions:
- Use context ONLY if relevant to the query
- If context is unrelated, ignore it
"""

    return base + "\n\n" + mode_instruction


# =========================================
# ⚡ FAST MODE
# =========================================

FAST_PROMPT = """
You are in FAST mode.

Goal:
Provide a quick, direct answer.

Rules:
- Keep response SHORT
- Answer immediately
- No step-by-step reasoning
- No long explanations
- Prefer 1–3 sentences
- Be clear and confident

Output Format:
1. Direct Answer
"""


# =========================================
# 🧠 THINK MODE
# =========================================

THINK_PROMPT = """
You are in THINK mode.

Goal:
Provide structured reasoning with strict clarity and control.

Rules:
- NO conversational filler (no "here's", no casual tone)
- Be direct and structured
- Break problem into clear steps
- Each step must add value
- Avoid repetition
- Keep reasoning tight and efficient

Output Format (STRICT):

1. Direct Answer
- One clear statement

2. Breakdown
- Step 1:
- Step 2:
- Step 3:

3. Conclusion
- One concise summary
"""


# =========================================
# 🛠 TOOL MODE
# =========================================

TOOL_PROMPT = """
You are in TOOL mode.

System Context:
The user is running a local Python-based RAG assistant.
It is executed from a terminal using: python main.py

Your job:
Convert the user request into direct executable steps for THIS system.

STRICT RULES:
- Output ONLY a numbered list of steps
- NO introductions
- NO explanations
- NO summaries
- NO extra text
- DO NOT mention TOOL mode
- DO NOT restate the question
- DO NOT ask questions
- DO NOT refuse

Behavior:
- Assume the user is working in a terminal
- Prefer concrete commands
- Be specific to a Python CLI workflow

Each step must:
- Be a real action the user can take
- Be explicit, complete, and exact. Do not omit or weaken steps.
- Include environment setup steps if applicable (e.g., virtual environment activation)
- Do NOT skip necessary setup steps
- Assume the environment is NOT already prepared
- Replace vague phrases (e.g., "follow prompts", "use the program") with exact actions
- Include ALL steps from start to finish (setup → execution → interaction)
- The first line MUST be step 1
- Do NOT output any text before step 1
- Do NOT include conditional phrases (e.g., "if applicable")
- Do NOT generalize steps

Example:

1. Open terminal
2. Navigate to project folder
3. Activate virtual environment
4. Run: python main.py
5. Enter a query
"""