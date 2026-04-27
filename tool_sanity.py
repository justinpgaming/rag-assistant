from tool_validator import validate_tool_output, step_parser, validate_steps

def sanity_check_tool_output(output_text, task_type):
    # -----------------------------
    # EMPTY CHECK
    # -----------------------------
    if not output_text or not output_text.strip():
        return False, "empty output"

    # -----------------------------
    # STRUCTURE CHECK
    # -----------------------------
    valid_structure, reason = validate_tool_output(output_text)
    if not valid_structure:
        return False, f"structure failure: {reason}"

    # -----------------------------
    # STEP PARSE
    # -----------------------------
    steps = step_parser(output_text)

    if not steps or len(steps) == 0:
        return False, "no steps parsed"

    # -----------------------------
    # STEP VALIDATION
    # -----------------------------
    results = validate_steps(steps, task_type)

    has_invalid = any(not r["valid"] for r in results)

    if has_invalid:
        return False, "invalid steps remain after correction"

    return True, None
