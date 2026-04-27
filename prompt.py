# =========================================
# 🧠 PROMPT SYSTEM
# =========================================

from templates import TASK_TEMPLATES

GLOBAL_PROMPT = """
SYSTEM ARCHITECTURE RULES:

1. MODE SEPARATION (STRICT)
- Tool Mode executes structured actions only
- Validator determines structural correctness only
- Correction fixes ONLY validator-reported structural violations
- Scoring evaluates quality only and must NOT influence correctness decisions

2. AUTHORITY HIERARCHY
- Validator is the only source of truth for structural validity
- Scoring is observational only
- Tool Mode does not validate correctness
- Correction does not define rules, only repairs violations

3. SHARED DEFINITIONS

3.1 ACTION UNIT DEFINITION
An "action" is:
- one physical operation
- applied to one primary object
- expressed as a single executable step

4. NON-OVERLAP RULE
- No rule should be defined differently across modules
"""

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


TOOL_PROMPT = GLOBAL_PROMPT + """
You are in TOOL mode.

FAILURE CONDITION:

If your response contains ANY text before "1." your answer is invalid and will be rejected.



CRITICAL OUTPUT RULE:

Your response MUST begin immediately with:
1.

- Output MUST start with "1." as the first character of the response
- Any text before "1." will cause immediate rejection
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
- Each step must contain only ONE action verb
- Do NOT combine actions using "and"


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
# PROMPT BUILDERS
# =========================================

# =========================================
# CORRECTION PROMPT
# =========================================


def build_correction_prompt(step_text: str, reason: str):
    return f"""
{GLOBAL_PROMPT}

Rewrite this step into a single, clear physical action.

STRICT RULES (MUST FOLLOW):
- Use EXACTLY ONE action verb
- Allowed verbs: pick, place, wipe, vacuum, sweep, remove, put, return
- Do NOT use more than one verb
- Do NOT use the word "and"
- Do NOT combine actions
- Do NOT use weak verbs like: organize, tidy, straighten, arrange
- Use a specific object (no "items", "things", "stuff")
- The action must be physically doable in one motion
- You must preserve the original meaning and object of the step
- You must NOT simplify to generic actions unless required by rules
- The corrected step must reflect the SAME task intent as the original

When correcting:
- If the original step contains multiple actions, reduce it to the FIRST atomic physical action only
- Do NOT invent unrelated actions
- Transform verbs to the closest allowed physical equivalent

FORMAT RULES:
- Output ONLY one sentence
- No explanations
- No labels like "Improved step"
- No extra text

BAD EXAMPLES (DO NOT DO):
- "Pick up clothes and put them away"
- "Straighten and arrange bedding"
- "Organize items on the desk"

GOOD EXAMPLES:
BAD EXAMPLES (DO NOT DO):
- "Pick up clothes and put them away"
- "Straighten and arrange bedding"
- "Organize items on the desk"
- "Pick up clothes from the floor"  ← ✅
- "Place books onto the bookshelf"  ← ✅
- "Vacuum the carpet to remove dirt"  ← ✅

Original step:
{step_text}

Reason it is bad:
{reason}

Corrected step:
"""

# ============================================
# GENERAL PROMPT BUILDER
3 ============================================

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
