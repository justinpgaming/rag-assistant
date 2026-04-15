current_task = None
task_queue = []


STOP_WORDS = {"how", "do", "does", "what", "is", "are", "the", "a", "an", "work", "works"}


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


def handle_focus(query):
    global current_task

    new_task = detect_task(query)

    if current_task is None:
        current_task = new_task
        return True, None

    if is_similar(current_task, new_task):
        return True, None

    return False, new_task


def set_task(task):
    global current_task
    current_task = task


def get_task():
    return current_task


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
