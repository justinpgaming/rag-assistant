results_summary = {
    "total": 0,
    "classifier_correct": 0,
    "validator_pass": 0,
    "validator_fail": 0,
    "constraint_routed_correctly": 0,
    "correction_used": 0,
    "correction_improved": 0,
}


TEST_CASES = [
    # ACTION (valid)
    "Pick up clothes and put them in the basket.",
    # ACTION (weak verb)
    "Clean the desk.",
    # ACTION (valid simple)
    "Vacuum the carpet.",
    # CONSTRAINT (should NOT go to validator)
    "Never place the observer where it cannot see the sugarcane grow.",
    # AMBIGUOUS / NOISE
    "Make sure everything is handled properly.",
]
def trace_classifier(text, classifier_fn):
    result = classifier_fn(text)
    print("\n🧭 CLASSIFIER")
    print("INPUT:", text)
    print("OUTPUT:", result)
    return result


def trace_validator(step, validate_fn):
    result = validate_fn([{"index": 0, "text": step}])[0]
    print("\n✅ VALIDATOR")
    print("INPUT:", step)
    print("OUTPUT:", result)
    return result


def trace_correction(step, reason, correct_fn, llm):
    result = correct_fn(step, reason, llm, {}, task_type="test")
    print("\n🔧 CORRECTION")
    print("INPUT:", step)
    print("OUTPUT:", result)
    return result


from classifier import classify_step  # adjust to your file
from tool_validator import validate_steps, correct_step


def run_pipeline_test():

    for i, text in enumerate(TEST_CASES):

        results_summary["total"] += 1

        print("\n==============================")
        print(f"CASE {i+1}")
        print("==============================")

        # 1. CLASSIFIER
        ctype = classify_step(text)

        print("🧭 TYPE:", ctype)

        # --- CLASSIFIER CHECK ---
        if "observer" in text or "never" in text.lower():
            expected = "CONSTRAINT"
        else:
            expected = "ACTION"

        if ctype == expected:
            results_summary["classifier_correct"] += 1

        # 2. ROUTING
        if ctype != "ACTION":
            print("➡️ NON-ACTION ROUTE")

            if ctype == "CONSTRAINT":
                results_summary["constraint_routed_correctly"] += 1

            continue

        # 3. VALIDATOR
        v = validate_steps([{"index": 0, "text": text}])[0]

        print("✅ VALIDATOR:", v)

        if v["valid"]:
            results_summary["validator_pass"] += 1
        else:
            results_summary["validator_fail"] += 1

            # 4. CORRECTION
            fixed = correct_step(
                text,
                v["reason"],
                llm_call_fn=mock_llm,
                experience_memory={},
                task_type="test",
            )

            results_summary["correction_used"] += 1

            # re-check validity
            v2 = validate_steps([{"index": 0, "text": fixed}])[0]

            if v2["valid"]:
                results_summary["correction_improved"] += 1


def print_summary():

    print("\n==============================")
    print("PIPELINE PASS / FAIL SUMMARY")
    print("==============================")

    total = results_summary["total"]

    def pct(x):
        return round((x / total) * 100, 2) if total else 0

    print(f"Total cases: {total}")

    print("\n🧭 Classifier Accuracy:")
    print(
        results_summary["classifier_correct"],
        "/",
        total,
        f"({pct(results_summary['classifier_correct'])}%)",
    )

    print("\n✅ Validator:")
    print("Pass:", results_summary["validator_pass"])
    print("Fail:", results_summary["validator_fail"])

    print("\n🔧 Correction:")
    print("Used:", results_summary["correction_used"])
    print("Improved:", results_summary["correction_improved"])

    print("\n📦 Constraint Routing:")
    print("Correctly routed:", results_summary["constraint_routed_correctly"])


if __name__ == "__main__":
    run_pipeline_test()
    print_summary()


#f __name__ == "__main__":
#   run_pipeline_test()
