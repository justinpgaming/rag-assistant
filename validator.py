import re

def is_valid_tool_output(text: str) -> bool:
    lines = [l.strip() for l in text.split("\n") if l.strip()]

    # Must be numbered list
    steps = []
    for line in lines:
        if line[0].isdigit() and "." in line:
            steps.append(line)

    if len(steps) < 4:
        return False

    # Reject obvious bad patterns only
    forbidden = [
        "think", "consider", "maybe", "you could",
        "prepare", "get ready", "take a deep breath"
    ]

    lowered = text.lower()
    if any(f in lowered for f in forbidden):
        return False

    return True