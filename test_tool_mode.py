# =========================================
# 🧪 TOOL MODE TEST RUNNER (CLEAN)
# =========================================

from main import run_tool_mode
from tool_validator import step_parser, validate_steps

# ---------------------------------
# TEST CASES
# ---------------------------------
TEST_CASES = [
    {
        "name": "clean_room_basic",
        "task": "clean my room",
        "task_type": "cleaning",
    },
    {
        "name": "clean_kitchen",
        "task": "clean the kitchen",
        "task_type": "cleaning",
    },
    {
        "name": "organize_desk",
        "task": "organize my desk",
        "task_type": "cleaning",
    },
]


# ---------------------------------
# RUN TESTS
# ---------------------------------
def run_tests():
    for test in TEST_CASES:
        print("\n" + "=" * 50)
        print(f"TEST: {test['name']}")
        print("=" * 50)

        # Run your actual system
        result = run_tool_mode(test["task"], [], test["task_type"])

        print("\nOUTPUT:\n")
        print(result)

        # -----------------------------
        # VALIDATION CHECK
        # -----------------------------
        steps = step_parser(result)
        validation = validate_steps(steps, test["task_type"])

        failures = [r for r in validation if not r["valid"]]

        if failures:
            print("\n❌ FAILURES:")
            for f in failures:
                print(f"- Step {f['index']}: {f['reason']}")
        else:
            print("\n✅ PASS")

        # -----------------------------
        # DUPLICATE DETECTION
        # -----------------------------
        seen = set()
        for step in steps:
            if step["text"] in seen:
                print(f"⚠ Duplicate step: {step['text']}")
            seen.add(step["text"])


# ---------------------------------
# ENTRY POINT
# ---------------------------------
if __name__ == "__main__":
    run_tests()
