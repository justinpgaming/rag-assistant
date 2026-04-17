# =========================================
# 🧠 RAG Assistant - Main Control Loop
# =========================================

print("🔥 THIS IS THE NEW VERSION 🔥")

from rag import load_data, retrieve
from llm import generate_answer
from memory import load_memory, add_goal, add_decision
from focus import (
    handle_focus, set_task, get_task,
    add_to_queue, view_queue, pop_next_task,
    set_mode, get_mode,
    set_control_mode, get_control_mode,
    complete_task
)
from logger import log_event
from viewer import view_logs
from prompt import build_prompt

import time
import re


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
        query: str = input("\n> ")
        print(f"DEBUG RAW INPUT: [{query}]")
        print("DEBUG: start of loop")

        mode = None
        skip_bypass = False
        is_tool_run = False

        is_command = query.strip().startswith("/")

        # -----------------------------
        # EXIT
        # -----------------------------
        if query.strip().lower() == "exit":
            return "exit"

        if query.strip().lower() == "/exit":
            print("👋 Exiting assistant...")
            return "exit"

        if not query.strip():
            continue

        # -----------------------------
        # MEMORY COMMANDS
        # -----------------------------
        if query.startswith("/add_goal "):
            goal = query.replace("/add_goal ", "").strip()
            add_goal(memory, goal)
            continue

        if query.startswith("/add_decision "):
            decision = query.replace("/add_decision ", "").strip()
            add_decision(memory, decision)
            continue

        # -----------------------------
        # OBSERVABILITY
        # -----------------------------
        if query.strip().lower() == "/view_last":
            view_logs(1)
            continue

        if query.strip().lower().startswith("/view_logs"):
            parts = query.strip().split()
            n = int(parts[1]) if len(parts) > 1 and parts[1].isdigit() else 5
            view_logs(n)
            continue

        # -----------------------------
        # MODE COMMANDS
        # -----------------------------
        if query.startswith("/set_mode "):
            new_mode = query.replace("/set_mode ", "").strip()

            if new_mode not in ["fast", "think", "tool"]:
                print("⚠ Invalid mode. Use: fast, think, tool")
                continue

            set_mode(new_mode)
            print(f"⚙ Thinking mode set to: {new_mode}")
            continue

        if query.strip().lower() == "/mode":
            print(f"🧭 Current mode: {get_mode()}")
            continue

        if query.strip().lower() == "/control":
            print(f"🧭 Control mode: {get_control_mode()}")
            continue

        if query.startswith("/set_control "):
            new_mode = query.replace("/set_control ", "").strip()
            set_control_mode(new_mode)
            continue

        # -----------------------------
        # SYSTEM COMMANDS
        # -----------------------------
        if query.strip().lower() == "/restart":
            print("\n🔄 Restarting assistant...\n")
            return "restart"

        # -----------------------------
        # /RUN (TOOL ENTRY POINT)
        # -----------------------------
        print("DEBUG: reached /run check")

        if query.strip().lower().startswith("/run "):
            task = query.strip()[5:].strip()

            if not task:
                print("⚠ Provide a task to run")
                continue

            print(f"\n🛠 Running task: {task}\n")

            query = f"{task}\n\nConstraints:\n- Do not assume tools, terminal, or environment unless explicitly stated."
            set_mode("tool")
            mode = "tool"
            skip_bypass = True
            is_tool_run = True

            # 🔒 TOOL GUARD (IMMEDIATE)
            vague_terms = {"thing", "things", "stuff", "it", "everything"}
            words = set(re.findall(r"\b\w+\b", query.lower()))

            if len(words) < 3 or words & vague_terms:
                print("⚠ Task too vague. Please be more specific.")
                continue

        # -----------------------------
        # COMMAND BYPASS
        # -----------------------------
        if is_command and not skip_bypass:
            continue

        # -----------------------------
        # FOCUS SYSTEM
        # -----------------------------
        allowed, new_task = handle_focus(query)

        if not allowed:
            current = get_task()
            control_mode = get_control_mode()

            if control_mode == "strict":
                print("\n🚫 Strict mode active — new task blocked")
                print(f"Current task: {current}")
                print(f"Blocked task: {new_task}")
                continue

            print("\n⚠ New task detected!")
            print(f"Current task: {current}")
            print(f"New task: {new_task}")
            print("\nChoose:")
            print("[1] Continue current task")
            print("[2] Switch to new task")
            print("[3] Add to queue")

            choice = input("> ").strip()

            if choice == "2":
                set_task(new_task)
                print("🔁 Switched to new task")
            elif choice == "3":
                add_to_queue(new_task)
                print("🔒 Staying on current task")
                continue
            else:
                print("🔒 Staying on current task")
                continue

        # -----------------------------
        # CORE RAG FLOW
        # -----------------------------
        mode = mode or get_mode()

        if mode == "tool":
            chunks = []
        else:
            chunks = retrieve(query, database)

        # -----------------------------
        # TASK TYPE HINT (MINIMAL)
        # -----------------------------
        task_type = "general"

        dev_keywords = {"python", "script", "code", "install", "package", "pip", "program"}

        words = set(query.lower().split())

        if words & dev_keywords:
            task_type = "development"

        prompt = build_prompt(query, chunks, mode, task_type=task_type)

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

        log_event(query, chunks, prompt, response_text)


        forbidden = ["terminal", "command prompt", "run:", "python --version"]

        if mode == "tool":
            lowered = response_text.lower()
            if any(f in lowered for f in forbidden):
                print("⚠ TOOL output violated constraints. Retrying...\n")

                # Regenerate once with stronger constraint
                query += "\n\nSTRICT: Do NOT include verification, terminal, or command usage."

                chunks = []
                prompt = build_prompt(query, chunks, mode)

                response_text = ""
                for chunk in generate_answer(prompt):
                    print(chunk, end="", flush=True)
                    response_text += chunk

                print()


if __name__ == "__main__":
    while True:
        result = main()

        if result == "restart":
            continue
        elif result == "exit":
            break