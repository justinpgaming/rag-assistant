# =========================================
# 🧠 PROMPT SYSTEM
# =========================================

FAST_PROMPT = """
You are in FAST mode.

- Give a direct, minimal answer
- No reasoning steps
- No explanations
"""


THINK_PROMPT = """
You are in THINK mode.

- Break the problem into steps
- Show clear reasoning
- No conversational filler
"""


TOOL_PROMPT = """
You are in TOOL mode.

HARD CONSTRAINTS:

- Output ONLY a numbered list starting at 1
- Minimum 5 steps
- No explanations or extra text


ACTION TYPES:

- Moving items (pick up, place, return)
- Cleaning actions (wipe, vacuum, dust)
- Reset actions (straighten, arrange, make bed)

All action types are valid when relevant.


QUALITY RULES:

- Each step must be a clear physical action
- Be specific about what is being moved or done
- Expand simple actions into visible steps
- Avoid vague phrases like "clean", "tidy", or "organize"
- Avoid repeating the same type of action
- Steps should follow a logical order


BAD EXAMPLES:
- "clean room"
- "organize stuff"
- "tidy surfaces"


GOOD EXAMPLES:
- "Pick up clothes from the floor and place them in the laundry hamper"
- "Place books from the desk onto the bookshelf"
- "Straighten bedsheets and arrange pillows neatly on the bed"
- "Wipe down the desk surface using a damp cloth"


DO NOT:
- include preparation steps
- include thinking or planning
- include tool setup unless required
"""

# =========================================
# PROMPT BUILDER
# =========================================

def build_prompt(query, context, mode, task_type="general"):
    mode_map = {
        "fast": FAST_PROMPT,
        "think": THINK_PROMPT,
        "tool": TOOL_PROMPT
    }

    mode_instruction = mode_map.get(mode, "")

    # -----------------------------
    # DEV TASK BOOST
    # -----------------------------
    if mode == "tool" and task_type == "development":
        mode_instruction += """

Additional rules for development tasks:
- The task is a software or programming setup task
- Do NOT create example scripts unless explicitly requested
- Focus on installation, configuration, and verification steps
- Include exact commands where applicable
- Include installation steps explicitly
- Include verification steps (e.g., checking version)
"""

    # -----------------------------
    # BASE PROMPT
    # -----------------------------
    if mode == "tool":
        base = f"""
Task Type: {task_type}

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

    return mode_instruction + base