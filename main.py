# =========================================
# 🧠 RAG Assistant - Main Control Loop
# =========================================

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
        query = input("\n> ")

        is_command = query.strip().startswith("/")

        if query.lower() == "exit":
            break

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
        # OBSERVABILITY COMMANDS
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
            break


        # -----------------------------
        # OVERRIDE COMMANDS
        # -----------------------------
        if query.startswith("/force_switch "):
            new_task = query.replace("/force_switch ", "").strip()
            set_task(new_task)
            print(f"⚡ Forced switch to: {new_task}")
            print("\n💡 Press Enter to run this task")

            follow_up = input("> ").strip()
            if follow_up == "":
                query = new_task
            else:
                continue

        if query.startswith("/force_queue "):
            new_task = query.replace("/force_queue ", "").strip()
            add_to_queue(new_task)
            print(f"⚡ Forced into queue: {new_task}")
            continue

        # -----------------------------
        # QUEUE COMMANDS
        # -----------------------------
        if query == "/queue":
            view_queue()
            continue

        if query == "/next":
            pop_next_task()
            continue

        if query == "/complete":
            complete_task()

            current = get_task()
            if current:
                print("\n💡 Press Enter to run this task")
                follow_up = input("> ").strip()

                if follow_up == "":
                    query = current
                else:
                    continue
            else:
                continue

        # -----------------------------
        # COMMAND BYPASS
        # -----------------------------
        if is_command:
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
        chunks = retrieve(query, database)
        mode = get_mode()
        prompt = build_prompt(query, chunks, mode)

        response_text = ""
        start_time = time.time()

        thinking_shown = False
        answer_started = False

        for chunk in generate_answer(prompt):

            # Show thinking only if needed
            if (
                mode != "fast"
                and not thinking_shown
                and not answer_started
                and time.time() - start_time > 0.5
            ):
                print("\nThinking...\n")
                thinking_shown = True

            # Print header when first token arrives
            if not answer_started:
                print("\n🤖 Answer:\n")
                answer_started = True

            print(chunk, end="", flush=True)
            response_text += chunk

        print()

        log_event(query, chunks, prompt, response_text)


if __name__ == "__main__":
    while True:
        main()
