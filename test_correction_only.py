import inspect

from memory_experience import (
    load_experience_memory,
    save_experience_memory,
    log_correction,
)
from tool_validator import (
    step_parser,
    validate_steps,
    apply_step_corrections,
    rebuild_output,
)

# -------------------------
# DEBUG MODE
# -------------------------
DEBUG = True


def debug(title, data=None):
    if DEBUG:
        print("\n" + "=" * 30)
        print(title)
        print("=" * 30)
        if data is not None:
            print(data)


# -------------------------
# LOAD MEMORY
# -------------------------
experience_memory = load_experience_memory()

# -------------------------
# INPUT
# -------------------------
raw_output = """1. Pick up clothes and put them in the basket.
2. Clean the desk.
3. Vacuum the carpet."""


# -------------------------
# MOCK LLM
# -------------------------
def mock_llm(prompt):
    if DEBUG:
        print("\n--- CORRECTION PROMPT ---")
        print(prompt)
        print("--------------------------\n")
    return "Pick up clothes from the floor"


# -------------------------
# STEP 1: PARSE
# -------------------------
steps = step_parser(raw_output)
debug("STEP 1 — PARSE", steps)

# -------------------------
# STEP 2: VALIDATE
# -------------------------
results = validate_steps(steps)
debug("STEP 2 — VALIDATION", results)

# -------------------------
# STEP 3: CORRECT
# -------------------------
corrected = apply_step_corrections(steps, results, mock_llm, experience_memory)

# -------------------------
# STEP 4: FINAL OUTPUT
# -------------------------
final_output = rebuild_output(corrected)
debug("STEP 3 — FINAL OUTPUT", final_output)

print("\nFINAL RESULT:\n")
print(final_output)

# -------------------------
# SAVE MEMORY
# -------------------------
save_experience_memory(experience_memory)
