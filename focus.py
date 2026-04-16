# =========================================
# 🧠 FOCUS SYSTEM
# =========================================
# Handles:
# - Task tracking
# - Task similarity detection
# - Focus enforcement (guided / strict)
# - Task queue
# - Mode systems (control + thinking)
# =========================================


# -----------------------------
# GLOBAL STATE
# -----------------------------
current_task = None
task_queue = []

CONTROL_MODE = "guided"   # guided | strict
THINKING_MODE = "fast"    # fast | think | tool


# -----------------------------
# TEXT PROCESSING
# -----------------------------
STOP_WORDS = {
    "how", "do", "does", "what", "is", "are",
    "the", "a", "an", "work", "works"
}


def normalize(text):
    words = text.lower().strip().split()

    cleaned = []
    for w in words:
        if w in STOP_WORDS:
            continue

        # simple plural normalization
        if w.endswith("s"):
            w = w[:-1]

        cleaned.append(w)

    return set(cleaned)


def is_similar(task1, task2, threshold=0.3):
    words1 = normalize(task1)
    words2 = normalize(task2)

    if not words1 or not words2:
        return False

    overlap = words1.intersection(words2)
    similarity = len(overlap) / min(len(words1), len(words2))

    return similarity >= threshold


def detect_task(query):
    return query.strip().lower()


# -----------------------------
# FOCUS LOGIC
# -----------------------------
def handle_focus(query):
    current = get_task()

    # No active task → set it
    if not current:
        set_task(query)
        return True, None

    new_task = query

    # Similar → allow
    if is_similar(current, new_task):
        return True, None

    # STRICT mode → block
    if get_control_mode() == "strict":
        return False, new_task

    # GUIDED mode → ask user
    return False, new_task


# -----------------------------
# TASK MANAGEMENT
# -----------------------------
def set_task(task):
    global current_task
    current_task = task


def get_task():
    return current_task


# -----------------------------
# QUEUE SYSTEM
# -----------------------------
def add_to_queue(task):
    global task_queue

    if task not in task_queue:
        task_queue.append(task)
        print(f"📌 Task added to queue: {task}")
    else:
        print("⚠ Task already in queue")


def view_queue():
    if not task_queue:
        print("📭 Queue is empty")
        return

    print("\n📋 Task Queue:")
    for i, task in enumerate(task_queue, 1):
        print(f"{i}. {task}")


def pop_next_task():
    global current_task

    if task_queue:
        current_task = task_queue.pop(0)
        print(f"▶ Now working on: {current_task}")
    else:
        print("📭 No tasks in queue")


def complete_task():
    global current_task

    if current_task is None:
        print("⚠ No active task to complete")
        return

    print(f"✅ Task completed: {current_task}")

    if task_queue:
        current_task = task_queue.pop(0)
        print(f"▶ Now working on: {current_task}")
    else:
        current_task = None
        print("📭 No more tasks in queue")


# -----------------------------
# MODE SYSTEM (CONTROL)
# -----------------------------
def set_control_mode(mode):
    global CONTROL_MODE

    if mode in ["guided", "strict"]:
        CONTROL_MODE = mode
        print(f"🧭 Control mode set to: {CONTROL_MODE}")
    else:
        print("⚠ Invalid control mode (guided / strict)")


def get_control_mode():
    return CONTROL_MODE


# -----------------------------
# MODE SYSTEM (THINKING)
# -----------------------------
def set_mode(mode):
    global THINKING_MODE

    if mode in ["fast", "think", "tool"]:
        THINKING_MODE = mode
    else:
        print("⚠ Invalid thinking mode (fast / think / tool)")


def get_mode():
    return THINKING_MODE
