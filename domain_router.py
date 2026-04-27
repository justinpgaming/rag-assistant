# domain_router.py


def route_domain(user_input: str) -> str:
    """
    Determines which domain the input belongs to.

    Current domains:
    - cleaning (default)
    - debug (basic detection)

    This is intentionally simple for now.
    """

    text = user_input.lower()

    # --- Debug detection (very basic for now) ---
    debug_keywords = [
        "error",
        "bug",
        "traceback",
        "exception",
        "fix",
        "crash",
    ]

    for word in debug_keywords:
        if word in text:
            return "debug"

    # --- Default fallback ---
    return "cleaning"
