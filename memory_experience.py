import json
import time

MAX_FAILURES = 1000


def log_correction(
    memory, original_step, failure_reason, attempted_fix, accepted, task_type=None
):
    if "corrections" not in memory:
        memory["corrections"] = []

    pattern = failure_reason.replace(" ", "_") if failure_reason else "unknown"

    entry = {
        "original_step": original_step,
        "failure_reason": failure_reason,
        "attempted_fix": attempted_fix,
        "accepted": accepted,
        "pattern": pattern,
        "task_type": task_type or "unknown",
        "score": 1 if accepted else -1,
    }

    # -------------------------
    # REMOVE OLD MATCHES
    # -------------------------
    memory["corrections"] = [
        e
        for e in memory["corrections"]
        if not (
            e["original_step"] == original_step
            and e["attempted_fix"] == attempted_fix
            and e["failure_reason"] == failure_reason
        )
    ]

    # -------------------------
    # ADD NEW ENTRY
    # -------------------------
    memory["corrections"].append(entry)

    # -------------------------
    # SAFETY CAP
    # -------------------------
    MAX_CORRECTIONS = 200
    if len(memory["corrections"]) > MAX_CORRECTIONS:
        memory["corrections"] = memory["corrections"][-MAX_CORRECTIONS:]

    # -------------------------
    # UPDATE PATTERN STATS
    # -------------------------
    if "patterns" not in memory or not isinstance(memory["patterns"], dict):
        memory["patterns"] = {}

    p = pattern

    if p not in memory["patterns"]:
        memory["patterns"][p] = {
            "attempts": 0,
            "success": 0,
            "score": 0.0,
        }

    memory["patterns"][p]["attempts"] += 1

    if accepted:
        memory["patterns"][p]["success"] += 1

    attempts = memory["patterns"][p]["attempts"]
    success = memory["patterns"][p]["success"]

    memory["patterns"][p]["score"] = round(success / attempts, 3)



def load_experience_memory():
    try:
        with open("memory_experience.json", "r") as f:
            data = json.load(f)

            if "corrections" not in data:
                data["corrections"] = []

            return data

    except:
        return {
            "failures": [],
            "patterns": {},
            "successes": [],
            "corrections": [],
            "meta": {"version": 1, "last_updated": None},
        }


def save_experience_memory(memory):
    memory["meta"]["last_updated"] = time.time()

    with open("memory_experience.json", "w") as f:
        json.dump(memory, f, indent=2)


def normalize(text):
    return text.lower().strip()


def is_duplicate(entry, memory):
    for f in memory["failures"]:
        if (
            normalize(f["step"]) == normalize(entry["step"])
            and f["reason"] == entry["reason"]
        ):
            return True
    return False


def update_memory_from_log(log, memory):
    for r in log.get("validation", []):

        text = r.get("text", "")

        # -------------------------
        # FILTER GARBAGE
        # -------------------------
        if not text or len(text) > 200:
            continue

        # -------------------------
        # FAILURE TRACKING
        # -------------------------
        if not r["valid"]:
            entry = {
                "step": text,
                "reason": r["reason"],
                "task_type": log.get("task_type", "unknown"),
            }

            if not is_duplicate(entry, memory):
                memory["failures"].append(entry)

        # -------------------------
        # SUCCESS TRACKING
        # -------------------------
        else:
            memory["successes"].append(
                {
                    "step": text,
                    "task_type": log.get("task_type", "unknown"),
                }
            )


    # -------------------------
    # CAP MEMORY SIZE
    # -------------------------
    if len(memory["failures"]) > MAX_FAILURES:
        memory["failures"] = memory["failures"][-MAX_FAILURES:]

    if len(memory["successes"]) > MAX_FAILURES:
        memory["successes"] = memory["successes"][-MAX_FAILURES:]


    #            if not is_duplicate(entry, memory):
    #                memory["failures"].append(entry)

    # cap memory size
    if len(memory["failures"]) > MAX_FAILURES:
        memory["failures"] = memory["failures"][-MAX_FAILURES:]

    return memory
