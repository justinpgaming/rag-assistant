import re

from memory_experience import log_correction

# -------------------------
# CONSTANTS
# -------------------------

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
    "sort",
}

GENERIC_PHRASES = [
    "the room",
    "remaining items",
    "correct locations",
    "various items",
    "miscellaneous",
]

VAGUE_OBJECTS = ["items", "things", "stuff"]


FIX_GUIDE = {
    "vague wording": "Replace vague phrases with specific objects and actions.",
    "too short": "Expand the step to include a clear action and object.",
    "weak verb": "Use a stronger, more direct action verb.",
    "invalid action combination": "Change the tool or object so the action makes sense.",
    "non-specific scope": "Remove words like 'any' or 'remaining' and be precise.",
    "unnatural phrasing": "Rewrite using natural, simple wording.",
    "weak verb with vague object": "Replace with a specific object and a clear physical action.",
    "redundant object grouping": "Use a single clear object instead of listing similar ones.",
}

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


def validate_steps(steps, task_type=None):
    results = []

    for step in steps:
        text = step["text"]
        words = re.findall(r"\b\w+\b", text.lower())

        valid = True
        reason = None

        has_weak = any(w in words for w in WEAK_VERBS)
        has_vague = any(w in words for w in VAGUE_WORDS)

        if has_weak:
            valid = False
            reason = "weak verb"
        elif has_vague:
            valid = False
            reason = "vague wording"

        ACTION_VERBS = ["pick", "place", "wipe", "vacuum", "sweep", "remove"]

        text_lower = text.lower()
        words = text_lower.split()

        has_action = any(v in text_lower for v in ACTION_VERBS)
        word_count = len(words)

        # -------------------------
        # SHORT STEP (allowed)
        # -------------------------
        SHORT_ALLOWED = word_count == 2 and words[0] in ACTION_VERBS

        # -------------------------
        # NORMAL STEP (detailed)
        # -------------------------
        LONG_ENOUGH = word_count >= 5

        # -------------------------
        # FINAL RULE
        # -------------------------
        if valid and not (has_action and (SHORT_ALLOWED or LONG_ENOUGH)):
            valid = False
            reason = "too short"

        # SAVE RESULT
        results.append(
            {
                "index": step["index"],
                "text": text,
                "valid": valid,
                "reason": reason,
            }
        )

    return results


# -------------------------
# STEP TYPE
# -------------------------


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
    prompt = build_correction_prompt(step_text, reason)

    # -------------------------
    # FIRST ATTEMPT
    # -------------------------
    corrected = llm_call_fn(prompt)

    print("\n🔧 RAW CORRECTION:", corrected)

    if not corrected:
        return step_text

    # -------------------------
    # SCORE FIRST ATTEMPT
    # -------------------------
    score = evaluate_step(corrected, step_text)
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

    if "desk" in cleaned and "carpet" in step_text:
        penalize

    if cleaned.lower() in [
        c["attempted_fix"].lower() for c in experience_memory.get("corrections", [])
    ]:
        print("❌ REJECTED (duplicate fix):", cleaned)

        log_correction(
            memory=experience_memory,
            original_step=step_text,
            failure_reason=reason,
            attempted_fix=cleaned,
            accepted=False,
            task_type=task_type,
        )

        return step_text

    # -------------------------
    # CLEAN RAW OUTPUT
    # -------------------------
    lines = [l.strip() for l in corrected.split("\n") if l.strip()]
    cleaned = lines[-1] if lines else ""

    lowered = cleaned.lower()

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

    # -------------------------
    # MIN LENGTH CHECK
    # -------------------------
    if len(cleaned.split()) < 4:
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

    # -------------------------
    # MUST START WITH ACTION
    # -------------------------
    VALID_STARTS = ("pick", "place", "wipe", "vacuum", "sweep", "remove")

    first_word = lowered.split()[0]

    if first_word not in VALID_STARTS:
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

    # -------------------------
    # LENGTH RULE
    # -------------------------
    words = lowered.split()

    SHORT_ALLOWED = len(words) == 2 and words[0] in VALID_STARTS
    LONG_ENOUGH = len(words) >= 4

    if not (SHORT_ALLOWED or LONG_ENOUGH):
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

    # -------------------------
    # FINAL SAFETY
    # -------------------------
    if any(x in cleaned for x in ["(", ")", ":"]):
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

    # -------------------------
    # CLEAN FINAL FORMAT
    # -------------------------
    if not cleaned.endswith("."):
        cleaned += "."

    if any(w in words for w in VAGUE_OBJECTS):
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

    # ✅ SUCCESS LOG
    log_correction(
        memory=experience_memory,
        original_step=step_text,
        failure_reason=reason,
        attempted_fix=cleaned,
        accepted=True,
        task_type=task_type,
    )
    return cleaned


def apply_step_corrections(steps, validation_results, llm_call_fn, experience_memory):
    corrected = []

    task_type = "cleaning"  # TEMP: or pass dynamically later

    for step, result in zip(steps, validation_results):
        step_text = step["text"]

        if result["valid"]:
            corrected.append(step_text)
            continue

        # First correction attempt
        fixed = correct_step(
            step_text,
            result["reason"],
            llm_call_fn,
            experience_memory,
            task_type=task_type,
        )

        # Score the corrected step
        score = evaluate_step(fixed, step_text)

        # Retry ONCE if score is too low
        if score < 70:
            retry_prompt = (
                f"Original step: {step_text}\n"
                f"Issue: {result['reason']}\n\n"
                f"Your previous correction was:\n{fixed}\n\n"
                f"It scored {score}/100.\n"
                f"Improve it. Return ONLY the corrected step."
            )

            improved = llm_call_fn(retry_prompt)

            # Re-score after retry
            retry_score = evaluate_step(improved, step_text)

            # Use the better result
            if retry_score >= score:
                fixed = improved
                score = retry_score

        # (Optional but aligned with roadmap) log score
        log_correction(
            original_step=step_text,
            failure_reason=result["reason"],
            attempted_fix=fixed,
            accepted=True,
            pattern=result["reason"],
            score=score,
        )

        corrected.append(fixed)

    return corrected


# -------------------------
# OUTPUT REBUILD
# -------------------------


def rebuild_output(corrected_steps):
    return "\n".join(f"{i+1}. {s}" for i, s in enumerate(corrected_steps))
