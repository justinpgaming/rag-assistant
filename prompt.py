# =========================================
# 🧠 PROMPT SYSTEM
# =========================================

from templates import TASK_TEMPLATES

FAST_PROMPT = """
You are in FAST mode.

- Give a direct, minimal answer
- No reasoning steps
- No explanations
"""


THINK_PROMPT = """
You are in THINK mode.

- Break the problem into steps
- Show ear reasoning
- No conversational filler
"""


TOOL_PROMPT = """
You are in TOOL mode.


CRITICAL OUTPUT RULE:

Your response MUST begin immediately with:
1.

- Do NOT output anything before "1."
- Do NOT output any introduction, header, or explanation.
- Do NOT include phrases like:
  "Here is", "Below is", "Task list", or similar
If you do, the output is invalid.

ENVIRONMENT ASSUMPTIONS:

- Assume a modern development environment
- Assume required software is already installed unless explicitly stated
- Focus only on actions relevant to the task
- Avoid unnecessary system-level setup or installation steps
- Do not include navigation or environment setup unless required

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
- Only include sequencing language (e.g., "then", "after", "starting with") when the order is required for the task
- NEVER use the word "clean" in any step
- Replace "clean" with specific actions such as:
  - sweep
  - vacuum
  - wipe
  - scrub


BAD EXAMPLES:
- "clean room"
- "organize stuff"
- "tidy surfaces"
- "Clean the floor"
- "Clean the room"


GOOD EXAMPLES:
- "Pick up clothes from the floor and place them in the laundry hamper"
- "Place books from the desk onto the bookshelf"
- "Straighten bedsheets and arrange pillows neatly on the bed"
- "Wipe down the desk surface using a damp cloth"
- "Sweep the floor using a broom to collect dust"
- "Vacuum the carpet to remove dirt"


DO NOT:
- include preparation steps
- include thinking or planning
- include tool setup unless required
"""

# =========================================
# PROMPT BUILDER
# =========================================


def build_prompt(query, context, mode, task_type="general"):
    mode_map = {"fast": FAST_PROMPT, "think": THINK_PROMPT, "tool": TOOL_PROMPT}
    mode_instruction = mode_map.get(mode, "")

    # -----------------------------
    # DEV TASK BOOST
    # -----------------------------
    if mode == "tool" and task_type == "development":
        mode_instruction += """

Additional rules for development tasks:
- The task is a software or programming setup task
- Do NOT create example scripts unless explicitly requested
- Focus on project-level actions, not system installation
- Do NOT install Python or system dependencies
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

    # -----------------------------
    # BUILD FINAL PROMPT
    # -----------------------------
    prompt = mode_instruction + base

    # -----------------------------
    # TEMPLATE INJECTION
    # -----------------------------
    template = TASK_TEMPLATES.get(task_type)

    if template:
        template_text = "\n".join(f"- {step}" for step in template)
    else:
        template_text = ""

    if mode == "tool" and template_text:
        prompt += f"\n\nTASK STRUCTURE:\nFollow this structure:\n{template_text}\n"

    return prompt
