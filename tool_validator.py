import re

VAGUE_WORDS = {
    "thing",
    "things",
    "stuff",
    "everything",
    "anything",
    "item",
    "items",
    "area",
    "spaces",
}

WEAK_VERBS = {
    "organize",
    "tidy",
    "clean",
    "fix",
    "handle",
    "manage",
    "arrange",
    "straighten",
}


GENERIC_PHRASES = [
    "the room",
    "remaining items",
    "correct locations",
    "various items",
    "miscellaneous",
]


FIX_GUIDE = {
    "vague wording": "Replace vague phrases with specific objects and actions.",
    "too short": "Expand the step to include a clear action and object.",
    "weak verb": "Use a stronger, more direct action verb.",
    "invalid action combination": "Change the tool or object so the action makes sense.",
    "non-specific scope": "Remove words like 'any' or 'remaining' and be precise.",
    "unnatural phrasing": "Rewrite using natural, simple wording.",
}

def validate_tool_output(text: str):
    lines = [line.strip() for line in text.split("\n") if line.strip()]

    if not lines:
        return False, "Empty output"

    # Must be numbered list
    if not all(re.match(r"^\d+\.", line) for line in lines):
        return False, "Output must be a numbered list starting at 1 with no extra text"

    # Must start at 1
    if not lines[0].startswith("1."):
        return False, "List must start at 1"

    # Minimum steps
    if len(lines) < 5:
        return False, "Too few steps (minimum 5 required)"

    return True, "OK"


def step_parser(raw_output: str):
    """
    Parses TOOL mode output into structured steps.

    Input:
        "1. Pick up clothes\n2. Wipe desk\n3. Vacuum floor"

    Output:
        [
            {"index": 1, "text": "Pick up clothes"},
            {"index": 2, "text": "Wipe desk"},
            {"index": 3, "text": "Vacuum floor"}
        ]
    """

    if not raw_output or not isinstance(raw_output, str):
        return []

    lines = raw_output.strip().split("\n")

    steps = []

    step_pattern = re.compile(r"^\s*(\d+)\.\s*(.*)$")

    for line in lines:
        match = step_pattern.match(line.strip())
        if not match:
            continue  # leave failure handling to validator

        index = int(match.group(1))
        text = match.group(2).strip()

        steps.append({"index": index, "text": text})

    return steps


def validate_steps(steps, task_type=None):
    results = []

    # -------------------------
    # STEP VALIDATION (per step)
    # -------------------------
    for step in steps:
        text = step["text"]
        words = text.lower().split()

        valid = True
        reason = None

        # RULES
        if any(w in words for w in WEAK_VERBS):
            valid = False
            reason = "weak verb"

        elif any(w in words for w in VAGUE_WORDS):
            valid = False
            reason = "vague wording"

        elif len(words) < 4:
            valid = False
            reason = "too short"

        # VAGUE PHRASES
        text_lower = text.lower()

        VAGUE_PHRASES = [
    "any remaining",
    "any visible",
    "misplaced items",
    "correct locations",
    "various items",
    "any other",
    "such as",
    "including",
]

        if valid and any(p in text_lower for p in VAGUE_PHRASES):
            valid = False
            reason = "vague wording"

        # INVALID COMBINATIONS
        INVALID_COMBINATIONS = [
            ("wipe", "trash"),
            ("wipe", "floor"),
            ("vacuum", "desk"),
            ("sweep", "desk"),
            ("sweep", "counter"),
            ("vacuum", "counter"),
            ("vacuum", "table"),
            ("sweep", "bed"),
        ]

        for verb, obj in INVALID_COMBINATIONS:
            if verb in words and obj in words:
                # allow valid spatial phrases like "around the desk"
                if "around" in words or "near" in words:
                    continue

                valid = False
                reason = f"invalid action combination: {verb} + {obj}"

        # UNNATURAL
        UNNATURAL_PATTERNS = [
            "edge of the",
            "corner of the",
            "onto the corner",
            "onto the edge",
        ]

        if valid and any(p in text_lower for p in UNNATURAL_PATTERNS):
            valid = False
            reason = "unnatural phrasing"

        # SUSPICIOUS
        SUSPICIOUS_WORDS = [
            "crumb-covered",
            "specific brand",
            "detailed description",
        ]

        if valid and any(w in text_lower for w in SUSPICIOUS_WORDS):
            valid = False
            reason = "hallucinated detail"

        # OBJECT RELATIONS
        INVALID_OBJECT_RELATIONS = [
            ("clothes", "bookshelf"),
            ("clothes", "shelf"),
            ("dishes", "bed"),
            ("books", "trash"),
        ]

        for obj, bad_target in INVALID_OBJECT_RELATIONS:
            if obj in words and bad_target in words:
                valid = False
                reason = f"invalid object placement: {obj} -> {bad_target}"

        # SAVE RESULT
        results.append({
            "index": step["index"],
            "text": text,
            "valid": valid,
            "reason": reason,
        })

    # -------------------------
    # SEQUENCE VALIDATION (after)
    # -------------------------
    REDUNDANT_PATTERNS = [
        ("pile", "organized"),
        ("neat pile", "organized"),
    ]

    for i in range(len(steps) - 1):
        prev_text = steps[i]["text"].lower()
        curr_text = steps[i + 1]["text"].lower()

        for a, b in REDUNDANT_PATTERNS:
            if a in prev_text and b in curr_text:
                results[i + 1]["valid"] = False
                results[i + 1]["reason"] = "redundant step"

    return results



def check_workflow(steps):
    """
    Detects logical issues between steps (does NOT modify them).
    Returns list of warnings.
    """

    warnings = []

    for i in range(len(steps) - 1):
        current = steps[i]["text"].lower()
        next_step = steps[i + 1]["text"].lower()

        # -------------------------
        # REDUNDANT ACTIONS
        # -------------------------
        if "pile" in current and "organize" in next_step:
            warnings.append(f"Step {i+2}: may be redundant after piling items")

        # -------------------------
        # ORDER ISSUES
        # -------------------------
        if "clean" in current and "place" in next_step:
            warnings.append(f"Step {i+2}: placing items after cleaning may be out of order")

        # -------------------------
        # INEFFICIENT SEQUENCE
        # -------------------------
        if "vacuum" in current and "pick up" in next_step:
            warnings.append(f"Step {i+2}: picking up items after vacuuming is inefficient")

    return warnings


def build_correction_prompt(step_text: str, reason: str):
    fix_instruction = FIX_GUIDE.get(reason, "Fix the step.")

    return f"""You are correcting a TOOL mode step.

- Use natural, normal human phrasing
- Do NOT over-specify unnecessary details
- Do not place objects in unrealistic locations (e.g., clothes on a bookshelf)
- Replace vague words with specific objects (e.g., "items" → "clothes", "papers", "dishes")

STRICT RULES:

- Output ONLY ONE step
- Do NOT include numbering
- Must be a physical action
- Must use a strong verb: pick up, place, wipe, vacuum, sweep
- Must include a specific object (clothes, desk, trash, carpet, etc.)
- Include a tool or target ONLY if it is natural and necessary
- Use the correct tool for the object (e.g., pick up papers, do not sweep or vacuum them)
- Do NOT combine actions (only one verb per step)

DO NOT:
- repeat other steps
- combine multiple actions
- invent new tasks
- use vague words: items, things, area, stuff
- use vague phrases: misplaced items, correct locations, any remaining, various items
- use incorrect tools for objects (e.g., sweeping a desk, vacuuming a table)

Fix the issue: {reason}
How to fix: {fix_instruction}

Original step:
"{step_text}"

Rewrite the step clearly and specifically.

Only output the corrected step.
"""

def correct_step(step_text: str, reason: str, llm_call_fn):
    prompt = build_correction_prompt(step_text, reason)
    corrected = llm_call_fn(prompt)

    if not corrected:
        return step_text

    cleaned = corrected.strip()

    # 🔥 HARD FILTER
    banned_phrases = ["here is", "corrected step", "i removed", "(", ")"]

    lowered = cleaned.lower()

    if any(p in lowered for p in banned_phrases):
        return step_text

    # enforce single line
    cleaned = cleaned.split("\n")[0].strip()

    return cleaned


def apply_step_corrections(steps, validation_results, llm_call_fn):
    corrected_steps = []

    for step, result in zip(steps, validation_results):

        if result["valid"]:
            corrected_steps.append(step["text"])
            continue

        # Try to fix step
        new_text = correct_step(step["text"], result["reason"], llm_call_fn)

        # 🔥 VALIDATE AGAIN
        recheck = validate_steps([{"index": step["index"], "text": new_text}])[0]

        if not recheck["valid"]:
            print(f"❌ Correction failed: {new_text} ({recheck['reason']})")
            corrected_steps.append(step["text"])
        else:
            corrected_steps.append(new_text)

    return corrected_steps


def rebuild_output(corrected_steps):
    """
    Rebuild numbered TOOL output.
    """

    lines = []

    for i, text in enumerate(corrected_steps, start=1):
        lines.append(f"{i}. {text}")

    return "\n".join(lines)
