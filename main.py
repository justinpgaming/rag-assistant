# =========================================
# 🧠 RAG Assistant - Main Control Loop
# CLEAN REBUILD
# =========================================

print("🔥 CLEAN MAIN LOADED 🔥")

from rag import load_data, retrieve
from llm import generate_answer
from memory import load_memory, add_goal, add_decision, add_idea, save_memory
from focus import (
    handle_focus,
    set_task,
    get_task,
    add_to_queue,
    set_mode,
    get_mode,
    set_control_mode,
    get_control_mode,
)
from logger import log_event
from viewer import view_logs
from prompt import build_prompt
from tool_validator import (
    validate_tool_output,  # keep for now
    step_parser,
    validate_steps,
    apply_step_corrections,
    rebuild_output,
)

import time
import re


def classify_task(query: str) -> str:
    q = query.lower()

    if any(k in q for k in ["clean", "room", "wash", "tidy"]):
        return "cleaning"
    elif any(
        k in q for k in ["setup", "set up", "install", "configure", "environment"]
    ):
        return "setup"
    elif any(k in q for k in ["python", "code", "script"]):
        return "development"
    else:
        return "general"


def stream_response(prompt, mode):
    start_time = time.time()

    if mode != "fast":
        print("\nThinking...\n")

    print("\n🤖 Answer:\n")

    response_text = generate_answer(prompt)

    print(response_text)

    return response_text


def run_tool_mode(query, chunks, task_type):
    attempts = 0
    max_attempts = 3

    while attempts < max_attempts:
        prompt = build_prompt(query, chunks, "tool", task_type=task_type)
        response_text = stream_response(prompt, "tool")

        # -----------------------------
        # STRUCTURE VALIDATION (GATE)
        # -----------------------------
        valid_structure, reason = validate_tool_output(response_text)

        if not valid_structure:
            print(f"\n⚠ Structure invalid: {reason}")
            print("⚠ Skipping correction (cannot safely parse)\n")
            return response_text

        # -----------------------------
        # STEP PARSING
        # -----------------------------
        steps = step_parser(response_text)

        # -----------------------------
        # STEP VALIDATION
        # -----------------------------
        results = validate_steps(steps, task_type)
        has_invalid = any(not r["valid"] for r in results)

        if not has_invalid:
            return response_text

        # -----------------------------
        # STEP CORRECTION
        # -----------------------------
        print("\n⚠ Invalid steps detected — applying corrections...\n")

        corrected_steps = apply_step_corrections(
            steps, results, lambda p: generate_answer(p)
        )

        # -----------------------------
        # REBUILD OUTPUT
        # -----------------------------
        response_text = rebuild_output(corrected_steps)

        return response_text

    print("❌ Failed after retries")
    return response_text


def main():
    print("🧠 Loading RAG system...")

    try:
        database = load_data()
    except Exception as e:
        print(f"❌ Failed to load data: {e}")
        return

    print(f"✅ Loaded {len(database)} chunks")

    memory = load_memory()
    save_memory(memory)
    print(
        f"🧠 Memory loaded: "
        f"{len(memory['goals'])} goals, "
        f"{len(memory['decisions'])} decisions, "
        f"{len(memory['ideas'])} ideas"
)

    while True:
        query = input("\n> ").strip()

        if not query:
            continue

        print(f"DEBUG RAW INPUT: [{query}]")

        mode = None
        skip_bypass = False

        # -----------------------------
        # EXIT
        # -----------------------------
        if query.lower() in ["exit", "/exit"]:
            print("👋 Exiting assistant...")
            return "exit"

        # -----------------------------
        # MEMORY COMMANDS
        # -----------------------------
        if query.startswith("/add_goal "):
            add_goal(memory, query.replace("/add_goal ", "").strip())
            continue

        if query.startswith("/add_decision "):
            add_decision(memory, query.replace("/add_decision ", "").strip())
            continue

        if query.startswith("/add_idea "):
            raw = query[len("/add_idea "):].strip()

            # optional category syntax: idea | category
            if "|" in raw:
                idea, category = [x.strip() for x in raw.split("|", 1)]
            else:
                idea = raw
                category = "general"

            add_idea(memory, idea, category)
            continue

        if query == "/view_ideas":
            if not memory["ideas"]:
                print("📭 No ideas yet")
            else:
                print("\n💡 Ideas:")
                for i, idea in enumerate(memory["ideas"], 1):
                    print(f"{i}. [{idea['category']}] {idea['text']}")
            continue

        if query == "/view_tasks":
            if not memory["tasks"]:
                print("📭 No tasks yet")
            else:
                print("\n🧩 Tasks:")
                for i, task in enumerate(memory["tasks"], 1):
                    print(f"{i}. {task}")
            continue

        # -----------------------------
        # OBSERVABILITY
        # -----------------------------
        if query == "/view_last":
            view_logs(1)
            continue

        if query.startswith("/view_logs"):
            parts = query.split()
            n = int(parts[1]) if len(parts) > 1 and parts[1].isdigit() else 5
            view_logs(n)
            continue

        # -----------------------------
        # MODE COMMANDS
        # -----------------------------
        if query.startswith("/set_mode "):
            new_mode = query.replace("/set_mode ", "").strip()

            if new_mode not in ["fast", "think", "tool"]:
                print("⚠ Invalid mode")
                continue

            set_mode(new_mode)
            print(f"⚙ Mode set to: {new_mode}")
            continue

        if query == "/mode":
            print(f"🧭 Current mode: {get_mode()}")
            continue

        if query.startswith("/set_control "):
            set_control_mode(query.replace("/set_control ", "").strip())
            continue

        # -----------------------------
        # TOOL MODE ENTRY
        # -----------------------------
        if query.startswith("/run "):
            task = query[5:].strip()

            if not task:
                print("⚠ Provide a task")
                continue

            print(f"\n🛠 Running task: {task}\n")

            # Vague guard
            vague_terms = {"thing", "things", "stuff", "it", "everything"}
            words = set(re.findall(r"\b\w+\b", task.lower()))

            if len(words) < 3 or words & vague_terms:
                print("⚠ Task too vague. Please be more specific.")
                continue

            query = task
            set_mode("tool")
            mode = "tool"
            skip_bypass = True

        # -----------------------------
        # COMMAND BYPASS
        # -----------------------------
        if query.startswith("/") and not skip_bypass:
            continue

        # -----------------------------
        # FOCUS SYSTEM
        # -----------------------------
        allowed, new_task = handle_focus(query)

        if not allowed:
            current = get_task()
            control_mode = get_control_mode()

            if control_mode == "strict":
                print("🚫 Strict mode — task blocked")
                continue

            print("\n⚠ New task detected!")
            print(f"Current: {current}")
            print(f"New: {new_task}")
            print("[1] Continue  [2] Switch  [3] Queue")

            choice = input("> ").strip()

            if choice == "2":
                set_task(new_task)
            elif choice == "3":
                add_to_queue(new_task)
                continue
            else:
                continue

        # -----------------------------
        # CORE FLOW
        # -----------------------------
        mode = mode or get_mode()

        if mode == "tool":
            chunks = []
        else:
            chunks = retrieve(query, database)

        # -----------------------------
        # TASK TYPE
        # -----------------------------
        task_type = classify_task(query)

        # -----------------------------
        # EXECUTION
        # -----------------------------
        if mode == "tool":
            response_text = run_tool_mode(query, chunks, task_type)
        else:
            prompt = build_prompt(query, chunks, mode, task_type=task_type)
            response_text = stream_response(prompt, mode)

        # -----------------------------
        # LOGGING
        # -----------------------------
        log_event(query, chunks, "prompt_hidden", response_text)


if __name__ == "__main__":
    while True:
        result = main()

        if result == "restart":
            continue
        elif result == "exit":
            break
