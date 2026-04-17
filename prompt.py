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

- Output must start at step 1
- Output ONLY a numbered list
- NO introductions
- NO explanations
- NO summaries
- NO extra text
- Do NOT restate the request
- Do NOT ask questions

STRICT EXECUTION RULES:

- Each step must be a direct action
- No optional language (no: "if needed", "if necessary", "of your choice")
- No suggestions or alternatives
- No branching logic
- No assumptions about user environment unless explicitly stated
- No vague actions
- Do NOT introduce new tools, interfaces, or environments not mentioned in the task

TASK TYPE RULES:

- If the request involves programming, installation, or software:
    → treat as DEVELOPMENT task
    → include exact commands
    → include install steps
    → include verification step ONLY if verification method is explicitly part of the task

- Otherwise:
    → treat as PHYSICAL task
    → do NOT include terminal, code, or software steps

FORMAT RULES:

- Each step must be one clear action
- No multi-action steps
- No code blocks
- Inline commands only

BAD EXAMPLE:
1. Install Python (if needed)

GOOD EXAMPLE:
1. Download Python from https://www.python.org/downloads/
2. Run the installer
3. Enable "Add Python to PATH"
4. Click "Install Now"
5. Open terminal
6. Run: python --version
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