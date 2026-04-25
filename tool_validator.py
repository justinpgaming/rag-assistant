import re

from memory_experience import log_correction

# -------------------------
# CONSTANTS
# -------------------------

LOCATION_HINTS = {
    "dresser": "in",
    "drawer": "in",
    "closet": "in",
    "shelf": "on",
    "bookshelf": "on",
    "table": "on",
    "desk": "on",
}

VAGUE_WORDS = {
    "thing",
    "things",
    "stuff",
    "everything",
    "anything",
    "item",
    "items",
    "misc",
    "miscellaneous",
    "remaining",
    "any",
}

# temporarily removed due to conflicts
REDUNDANT_PATTERNS = [
    #    "to remove",
    #    "to clean",
    #    "to collect",
    #    "to pick up",
]

WEAK_VERBS = {
    "organize",
    "tidy",
    "clean",
    "fix",
    "handle",
    "manage",
    "sort",
}

GENERIC_PHRASES = [
    "the room",
    "remaining items",
    "correct locations",
    "various items",
    "miscellaneous",
]

BANNED_PHRASES = [
    "here is",
    "here's",
    "below is",
    "task list",
    "steps:",
    "improved step",
    "corrected step",
    "items",
    "things",
    "correct locations",
    "visible items",
    "any remaining",
    "remaining items",
    "leftover items",
    "where they belong",
    "correct locations",
    "any items",
    "items",
    "in the room",
]

VAGUE_OBJECTS = ["items", "things", "stuff"]


ACTION_VERBS = [
    "pick",
    "place",
    "wipe",
    "vacuum",
    "sweep",
    "remove",
    "put",
    "return",
    "arrange",
    "straighten",
    "tuck",
    "align",
    "dust",
    "scrub",
]


INVALID_ACTIONS = [
    ("remove", "carpet"),
    ("wipe", "bed"),
    ("vacuum", "trash"),
]

FIX_GUIDE = {
    "vague wording": "Replace vague phrases with specific objects and actions.",
    "too short": "Expand the step to include a clear action and object.",
    "weak verb": "Use a stronger, more direct action verb.",
    "invalid action combination": "Change the tool or object so the action makes sense.",
    "non-specific scope": "Remove words like 'any' or 'remaining' and be precise.",
    "unnatural phrasing": "Rewrite using natural, simple wording.",
    "weak verb with vague object": "Replace with a specific object and a clear physical action.",
    "redundant object grouping": "Use a single clear object instead of listing similar ones.",
    "multiple actions": "Split into one clear action. Do not combine actions.",
}


# -------------------------
# CORRECTION PROMPT
# -------------------------


def build_correction_prompt(step_text: str, reason: str):
    return f"""
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
- "Pick up clothes from the floor and place them in the laundry hamper"  ← ❌ (still bad, shows why multi-action is wrong)
- "Pick up clothes from the floor"  ← ✅
- "Place books onto the bookshelf"  ← ✅
- "Vacuum the carpet to remove dirt"  ← ✅

Original step:
{step_text}

Reason it is bad:
{reason}

Corrected step:
"""


# -------------------------
# STEP EVALUATION
# -------------------------


def evaluate_step(step, original_step):
    score = 100

    words = step.lower().strip().split()

    VALID_STARTS = (
        "pick",
        "place",
        "wipe",
        "vacuum",
        "sweep",
        "remove",
        "put",
        "return",
    )

    # ❌ multiple actions (hard fail)
    if " and " in step.lower():
        score -= 40

    #    if " to " in step.lower():
    #        score -= 20

    # ❌ empty step
    if not words:
        return 0

    # ❌ weak start
    if words[0] not in VALID_STARTS:
        score -= 30

    SHORT_ALLOWED = len(words) >= 2 and words[0] in VALID_STARTS

    if not SHORT_ALLOWED and len(words) < 4:
        score -= 25

    # ❌ vague words
    VAGUE_OBJECTS = ["things", "stuff", "items"]
    if any(w in words for w in VAGUE_OBJECTS):
        score -= 25

    # ❌ missing period
    if not step.endswith("."):
        score -= 10

    return max(0, min(100, score))


# -------------------------
# OUTPUT VALIDATION
# -------------------------


def validate_tool_output(text: str):
    lines = [line.strip() for line in text.split("\n") if line.strip()]

    if not lines:
        return False, "Empty output"

    if not all(re.match(r"^\d+\.", line) for line in lines):
        return False, "Output must be a numbered list"

    if not lines[0].startswith("1."):
        return False, "List must start at 1"

    if len(lines) < 5:
        return False, "Too few steps"

    return True, "OK"


# -------------------------
# PARSER
# -------------------------


def step_parser(raw_output: str):
    if not raw_output or not isinstance(raw_output, str):
        return []

    steps = []
    pattern = re.compile(r"^\s*(\d+)\.\s*(.*)$")

    for line in raw_output.split("\n"):
        match = pattern.match(line.strip())
        if not match:
            continue

        steps.append({"index": int(match.group(1)), "text": match.group(2).strip()})

    return steps


# -------------------------
# STEP VALIDATION
# -------------------------
def count_action_verbs(text: str):
    words = re.findall(r"\b\w+\b", text.lower())

    count = 0
    hits = []

    for i, w in enumerate(words):
        if any(w.startswith(v) for v in ACTION_VERBS):
            count += 1
            hits.append(w)

        # 👇 detect "to remove", "to collect", etc
        if w == "to" and i + 1 < len(words):
            next_word = words[i + 1]
            if any(next_word.startswith(v) for v in ACTION_VERBS):
                count += 1
                hits.append(f"to_{next_word}")

    return count, hits


def validate_steps(steps, task_type=None):
    print("\n=== VALIDATION START ===")

    results = []

    INVALID_ACTIONS = [
        ("remove", "carpet"),
        ("wipe", "bed"),
        ("vacuum", "trash"),
    ]

    for step in steps:
        text = step["text"]
        text_lower = text.lower()

        # 🔍 DEBUG HEADER (safe + structured)
        print("\n=== STEP START ===")
        print(f"RAW: {text}")
        print(f"NORMALIZED: {text_lower}")

        words = re.findall(r"\b\w+\b", text_lower)
        word_count = len(words)

        valid = True
        reason = None

        # -------------------------
        # INVALID ACTION COMBO
        # -------------------------
        for verb, obj in INVALID_ACTIONS:
            if verb in text_lower and obj in text_lower:
                print(f"INVALID MATCH: {verb} + {obj}")
                valid = False
                reason = "invalid action combination"
                break

        # -------------------------
        # MULTIPLE ACTION (HARD RULE)
        # -------------------------
        if valid:
            verb_count, _ = count_action_verbs(text)

            if verb_count > 1:
                valid = False
                reason = "multiple actions"

        # -------------------------
        # PURPOSE / CHAINED ACTIONS
        # -------------------------
        if valid and " to " in text_lower:
            valid = False
            reason = "multiple actions"

        if valid and "," in text_lower:
            valid = False
            reason = "multiple actions"

        # -------------------------
        # WEAK / VAGUE WORDING
        # -------------------------
        if valid and any(w in words for w in WEAK_VERBS):
            valid = False
            reason = "weak verb"

        if valid and any(w in words for w in VAGUE_WORDS):
            valid = False
            reason = "vague wording"

        if valid and any(
            w in text_lower
            for w in ["items", "things", "stuff", "anything", "any", "remaining"]
        ):
            valid = False
            reason = "vague wording"

        # -------------------------
        # BANNED PHRASES
        # -------------------------
        if valid and any(p in text_lower for p in BANNED_PHRASES):
            valid = False
            reason = "non-specific scope"

        if valid and any(p in text_lower for p in REDUNDANT_PATTERNS):
            valid = False
            reason = "redundant phrasing"

        if valid and "remove dirt" in text_lower:
            valid = False
            reason = "missing tool"

        # -------------------------
        # LENGTH / ACTION RULE
        # -------------------------
        if valid:
            has_action = any(v in text_lower for v in ACTION_VERBS)

            SHORT_ALLOWED = word_count == 2 and words[0] in ACTION_VERBS
            LONG_ENOUGH = word_count >= 3

            if not (has_action and (SHORT_ALLOWED or LONG_ENOUGH)):
                valid = False
                reason = "too short"

        print(f"RESULT: valid={valid}, reason={reason}")

        results.append(
            {
                "index": step["index"],
                "text": text,
                "valid": valid,
                "reason": reason,
            }
        )

    return results


def get_step_type(step_text: str) -> str:
    s = step_text.lower()

    if any(w in s for w in ["wipe", "wash", "vacuum", "sweep"]):
        return "clean"

    if any(w in s for w in ["pick up", "pickup", "gather", "collect", "remove"]):
        return "pickup"

    if any(w in s for w in ["place", "organize", "arrange", "put"]):
        return "organize"

    return "other"


# -------------------------
# WORKFLOW CHECK
# -------------------------


def check_workflow(steps):
    warnings = []

    last_type = None
    seen_types = []
    seen_objects = {}

    for i, step in enumerate(steps):
        text = step["text"]
        current_type = get_step_type(text)

        print(f"{i+1}: {text} -> {current_type}")  # DEBUG

        words = re.findall(r"\b\w+\b", text.lower())

        key = None
        for w in words:
            if w in ["paper", "papers", "document", "documents"]:
                key = "papers"
                break
            if w in ["trash", "garbage"]:
                key = "trash"
                break

        if key is None:
            key = words[-1] if words else ""

        if key in seen_objects:
            warnings.append(f"Step {i+1}: repeated work on '{key}'")

        seen_objects[key] = i

        if current_type == "pickup" and "clean" in seen_types:
            warnings.append(f"Step {i+1}: pickup occurs after cleaning")

        if last_type == "clean" and current_type == "pickup":
            warnings.append(f"Step {i+1}: workflow goes backward")

        seen_types.append(current_type)
        last_type = current_type

    return warnings


def correct_step(
    step_text: str, reason: str, llm_call_fn, experience_memory, task_type=None
):

    print("🔍 START:", step_text)
    prompt = build_correction_prompt(step_text, reason)

    # -------------------------
    # FIRST ATTEMPT
    # -------------------------
    corrected = llm_call_fn(prompt)

    # print("\n🔧 RAW CORRECTION:", corrected)

    if not corrected:
        return step_text

    # -------------------------
    # CLEAN RAW OUTPUT (MUST BE AFTER CHECK)
    # -------------------------
    lines = [l.strip() for l in corrected.split("\n") if l.strip()]
    cleaned = lines[-1] if lines else ""
    lowered = cleaned.lower()

    # -------------------------
    # SCORE FIRST ATTEMPT
    # -------------------------
    score = evaluate_step(cleaned, step_text)
    print(f"📊 Score: {score}/100")
    # -------------------------
    # RETRY IF LOW SCORE
    # -------------------------
    if score < 70:
        retry_prompt = (
            prompt + f"\n\nYour previous attempt scored {score}/100.\n"
            "Improve it. Make it more specific, more physical, and follow ALL rules strictly."
        )

        corrected_retry = llm_call_fn(retry_prompt)

        print("\n🔁 RETRY CORRECTION:", corrected_retry)

        if corrected_retry:
            retry_score = evaluate_step(corrected_retry, step_text)
            print(f"📊 Retry Score: {retry_score}/100")

            # keep the better one
            if retry_score > score:
                corrected = corrected_retry
                score = retry_score

    # -------------------------
    # PREVENT GENERIC REUSE
    # (your existing logic continues below)
    # -------------------------

    #    if cleaned.lower() in [
    #        c["attempted_fix"].lower() for c in experience_memory.get("corrections", [])
    #    ]:
    #        print("❌ REJECTED (duplicate fix):", cleaned)

    #        log_correction(
    #            memory=experience_memory,
    #            original_step=step_text,
    #            failure_reason=reason,
    #            attempted_fix=cleaned,
    #            accepted=False,
    #            task_type=task_type,
    #        )

    #        return step_text

    # -------------------------
    # HARD FILTER
    # -------------------------
    banned_phrases = [
        "here is",
        "corrected step",
        "revised step",
        "i fixed",
        "i changed",
    ]

    if any(p in lowered for p in banned_phrases):
        print("❌ REJECTED:", cleaned)

        log_correction(
            memory=experience_memory,
            original_step=step_text,
            failure_reason=reason,
            attempted_fix=cleaned,
            accepted=False,
            task_type=task_type,
        )

        return step_text

    print("➡️ ENTERING STRUCTURE:", cleaned)

    # -------------------------
    # BASIC STRUCTURE CHECKS
    # -------------------------
    words = lowered.split()

    VALID_STARTS = ("pick", "place", "wipe", "vacuum", "sweep", "remove")

    if not words:
        return step_text

    # must start with valid verb
    if words[0] not in VALID_STARTS:
        print("❌ REJECTED:", cleaned)
        return step_text

    # allow short but valid actions (like "vacuum carpet")
    SHORT_ALLOWED = len(words) >= 2 and words[0] in VALID_STARTS
    LONG_ENOUGH = len(words) >= 4

    if not (SHORT_ALLOWED or LONG_ENOUGH):
        print("❌ REJECTED:", cleaned)
        return step_text

    # reject vague objects
    if any(w in words for w in VAGUE_OBJECTS):
        print("❌ REJECTED:", cleaned)
        return step_text

    # safety filter
    if any(x in cleaned for x in ["(", ")", ":"]):
        print("❌ REJECTED:", cleaned)
        return step_text

    # ensure period
    if not cleaned.endswith("."):
        cleaned += "."

    # ✅ SUCCESS LOG
    log_correction(
        memory=experience_memory,
        original_step=step_text,
        failure_reason=reason,
        attempted_fix=cleaned,
        accepted=True,
        task_type=task_type,
    )

    for obj, correct_prep in LOCATION_HINTS.items():
        if obj in lowered:
            if f"on the {obj}" in lowered and correct_prep == "in":
                cleaned = cleaned.replace(f"on the {obj}", f"in the {obj}")
            elif f"in the {obj}" in lowered and correct_prep == "on":
                cleaned = cleaned.replace(f"in the {obj}", f"on the {obj}")
    return cleaned


def apply_step_corrections(steps, validation_results, llm_call_fn, experience_memory):
    corrected = []
    task_type = "cleaning"  # TEMP

    for step, result in zip(steps, validation_results):
        step_text = step["text"]  # ALWAYS FIRST

        # -------------------------
        # IF ALREADY VALID → KEEP
        # -------------------------
        if result["valid"]:
            corrected.append(step_text)
            continue

        # -------------------------
        # FIRST CORRECTION ATTEMPT
        # -------------------------
        fixed = correct_step(
            step_text,
            result["reason"],
            llm_call_fn,
            experience_memory,
            task_type=task_type,
        )

        # -------------------------
        # VALIDATE CORRECTION
        # -------------------------
        fixed_eval = validate_steps([{"index": 0, "text": fixed}])[0]

        # -------------------------
        # SCORE CORRECTION
        # -------------------------
        score = evaluate_step(fixed, step_text)

        # -------------------------
        # RETRY ONCE IF BAD
        # -------------------------
        if not fixed_eval["valid"] or score < 60:
            retry_prompt = (
                f"Original step: {step_text}\n"
                f"Issue: {result['reason']}\n\n"
                f"Your previous correction was:\n{fixed}\n\n"
                f"It scored {score}/100.\n"
                f"Improve it. Return ONLY the corrected step."
            )

            improved = llm_call_fn(retry_prompt)

            if improved:
                retry_eval = validate_steps([{"index": 0, "text": improved}])[0]
                retry_score = evaluate_step(improved, step_text)

                print(f"🔁 Retry Score: {retry_score}/100")

                if retry_eval["valid"] and retry_score >= score:
                    fixed = improved
                    score = retry_score
                    fixed_eval = retry_eval

        # -------------------------
        # DECISION BLOCK
        # -------------------------
        orig = step_text

        # HARD RULE: never allow multi-action
        if result["reason"] == "multiple actions":
            final = fixed

        elif fixed_eval["valid"]:
            final = fixed

        else:
            final = fixed if score >= 60 else orig

        # -------------------------
        # SAVE RESULT
        # -------------------------
        corrected.append(final)

    return corrected


def rebuild_output(corrected_steps):
    return "\n".join(f"{i+1}. {s}" for i, s in enumerate(corrected_steps))


if __name__ == "__main__":
    count, hits = count_action_verbs("vacuum the carpet to remove dirt")
    print("DEBUG:", count, hits)
