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
    "surface",
}

WEAK_VERBS = {"organize", "tidy", "clean", "fix", "handle", "manage"}


GENERIC_PHRASES = [
    "the room",
    "remaining items",
    "correct locations",
    "various items",
    "miscellaneous",
]


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


def validate_steps(steps):
    results = []

    for step in steps:
        text = step["text"]
        words = text.lower().split()

        valid = True
        reason = None

        # -------------------------
        # RULES
        # -------------------------

        if any(w in words for w in WEAK_VERBS):
            valid = False
            reason = "weak verb"

        elif any(w in words for w in VAGUE_WORDS):
            valid = False
            reason = "vague wording"

        elif len(words) < 4:
            valid = False
            reason = "too short"

        # -------------------------
        # INVALID COMBINATIONS
        # -------------------------

        INVALID_COMBINATIONS = [
            ("wipe", "trash"),
            ("wipe", "floor"),
            ("vacuum", "desk"),
            ("sweep", "desk"),
        ]

        for verb, obj in INVALID_COMBINATIONS:
            if verb in words and obj in words:
                valid = False
                reason = f"invalid action combination: {verb} + {obj}"

        # -------------------------
        # SAVE RESULT (INSIDE LOOP)
        # -------------------------

        results.append(
            {
                "index": step["index"],
                "text": text,
                "valid": valid,
                "reason": reason,
            }
        )

    return results


def build_correction_prompt(step_text: str, reason: str):
    return f"""You are correcting a TOOL mode step.

STRICT RULES:

- Output ONLY ONE step
- Do NOT include numbering
- Must be a physical action
- Must use a strong verb: pick up, place, wipe, vacuum, sweep
- Must include a specific object (clothes, desk, trash, carpet, etc.)
- Must include a target or tool (into, onto, using, with)

DO NOT:
- repeat other steps
- combine multiple actions
- invent new tasks
- use vague phrases like "items", "things", "area"

Fix the issue: {reason}

Original step:
"{step_text}"
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
            # fallback: keep original (controlled failure)
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
