from tool_validator import (
    step_parser,
    validate_steps,
    apply_step_corrections,
    rebuild_output,
)

raw_output = """1. Remove trash from the floor and place it in the bin.
2. Pick up clothes from the floor.
3. Clean the desk.
4. Arrange items neatly.
5. Vacuum the carpet thoroughly."""


def mock_llm(prompt):
    print("\n--- CORRECTION PROMPT ---")
    print(prompt)
    print("-------------------------\n")
    return "Wipe the desk surface using a cloth"


# STEP 1: Parse
steps = step_parser(raw_output)
print("PARSED STEPS:")
print(steps)

# STEP 2: Validate
results = validate_steps(steps)
print("\nVALIDATION RESULTS:")
for r in results:
    print(r)

# STEP 3: Correct
corrected = apply_step_corrections(steps, results, mock_llm)

# STEP 4: Rebuild
print("\nFINAL OUTPUT:\n")
print(rebuild_output(corrected))
