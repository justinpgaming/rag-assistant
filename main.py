# =========================================
# 🧠 RAG Assistant - Main Control Loop
# CLEAN REBUILD
# =========================================

print("🔥 CLEAN MAIN LOADED 🔥")

from rag import load_data, retrieve
from llm import generate_answer
from memory import load_memory, add_goal, add_decision
from focus import (
    handle_focus, set_task, get_task,
    add_to_queue,
    set_mode, get_mode,
    set_control_mode, get_control_mode,
)
from logger import log_event
from viewer import view_logs
from prompt import build_prompt
from validator import is_valid_tool_output

import time
import re


def stream_response(prompt, mode):
    response_text = ""
    start_time = time.time()

    thinking_shown = False
    answer_started = False

    for chunk in generate_answer(prompt):

        if (
            mode != "fast"
            and not thinking_shown
            and not answer_started
            and time.time() - start_time > 0.5
        ):
            print("\nThinking...\n")
            thinking_shown = True

        if not answer_started:
            print("\n🤖 Answer:\n")
            answer_started = True

        print(chunk, end="", flush=True)
        response_text += chunk

    print()
    return response_text


def run_tool_mode(query, chunks, task_type):
    attempts = 0
    max_attempts = 2

    while attempts <= max_attempts:
        prompt = build_prompt(query, chunks, "tool", task_type=task_type)
        response_text = stream_response(prompt, "tool")

        valid = is_valid_tool_output(response_text)

        if valid:
            return response_text

        print("⚠ Invalid TOOL output. Retrying...\n")

        query += """

STRICT TOOL RULES (MANDATORY):

- Output ONLY a numbered list
- Minimum 5 steps
- Each step must be a clear physical action
- No vague steps like "clean room" or "organize"
- No preparation steps
- No tool setup unless explicitly required
"""

        attempts += 1

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
    print(f"🧠 Memory loaded: {len(memory['goals'])} goals, {len(memory['decisions'])} decisions")

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

        # Task type hint
        task_type = "general"
        dev_keywords = {"python", "code", "install", "pip", "script"}

        if set(query.lower().split()) & dev_keywords:
            task_type = "development"

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