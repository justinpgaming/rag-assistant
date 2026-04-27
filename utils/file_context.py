def get_file_context(file_path: str, line_number: int, radius: int = 5):
    """
    Returns lines around a given line number.

    radius = number of lines before and after
    """

    try:
        with open(file_path, "r") as f:
            lines = f.readlines()

        total_lines = len(lines)

        # Adjust for 0-based index
        target_index = line_number - 1

        start = max(0, target_index - radius)
        end = min(total_lines, target_index + radius + 1)

        context = []

        for i in range(start, end):
            line_num = i + 1
            prefix = ">> " if i == target_index else "   "
            context.append(f"{prefix}{line_num}: {lines[i].rstrip()}")

        return "\n".join(context)

    except Exception as e:
        return f"ERROR LOADING FILE: {e}"
