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
    check_workflow,
    step_parser,
    validate_steps,
    apply_step_corrections,
    rebuild_output,
)
from memory_experience import (
    load_experience_memory,
    save_experience_memory,
    update_memory_from_log,
    load_experience_memory,
)

from tool_sanity import sanity_check_tool_output
from domain_router import route_domain
from debug_mode import run_debug_mode

from teach_mode import teach_mode
import time
import re

system_files = ["tool_validator.py"]


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
    # --- DOMAIN ROUTING (NEW) ---
    domain = route_domain(query)
    print(f"[DOMAIN] {domain}")

    attempts = 0
    max_attempts = 3


    # --- DOMAIN BEHAVIOR CONTROL (NEW) ---
    if domain == "debug":
        print("[ROUTE] Redirecting to debug mode")
        return run_debug_mode(query, generate_answer)

    while attempts < max_attempts:
        attempts += 1

        prompt = build_prompt(query, chunks, "tool", task_type=task_type)
        response_text = stream_response(prompt, "tool")

        # STRUCTURE VALIDATION
        valid_structure, reason = validate_tool_output(response_text)

        if not valid_structure:
            print(f"\n❌ STRUCTURE FAILURE: {reason}")
            print("❌ Output rejected — invalid tool format\n")
            return "[ERROR] Invalid tool output structure"

        # STEP PARSING
        steps = step_parser(response_text)

        # STEP VALIDATION
        results = validate_steps(steps, task_type)

        print("DEBUG results:", results)

        has_invalid = any(not r["valid"] for r in results)

        # EXPERIENCE MEMORY
        experience_memory = load_experience_memory()
        log = {"task_type": task_type, "validation": results}
        experience_memory = update_memory_from_log(log, experience_memory)
        save_experience_memory(experience_memory)

        # WORKFLOW CHECK
        workflow_warnings = check_workflow(steps)

        if not has_invalid:
            final_output = response_text
        else:
            print("\n⚠ Invalid steps detected — applying corrections...\n")

            corrected_steps = apply_step_corrections(
                steps, results, lambda p: generate_answer(p), experience_memory
            )

            final_output = rebuild_output(corrected_steps)

        # FINAL CHECK
        final_steps = step_parser(final_output)

        print("\n--- FINAL STEPS FOR WORKFLOW ---")
        for s in final_steps:
            print(s)

        workflow_warnings = check_workflow(final_steps)

        if workflow_warnings:
            print("\n⚠ Workflow Warnings:")
            for w in workflow_warnings:
                print(f"- {w}")

        # -----------------------------
        # FINAL SANITY CHECK
        # -----------------------------
        if domain == "cleaning":
            is_valid, reason = sanity_check_tool_output(final_output, task_type)
        else:
            is_valid, reason = True, None

        if not is_valid:
            print(f"\n🚨 SANITY CHECK FAILED: {reason}")

            # Optional fallback
            return "[ERROR] Tool output failed final validation"

        print("✅ SANITY CHECK PASSED")

        return final_output


def run_pipeline(query, *args, **kwargs):
    print("DEBUG RAW INPUT:", query)

    # -----------------------------
    # 🔥 HARD DEBUG OVERRIDE (TOP PRIORITY)
    # -----------------------------
    print("RAW INPUT:", query)

    if query.strip().startswith("/debug"):
        print("DEBUG ROUTE TRIGGERED")
        print("FORCED DEBUG MODE")

        from llm import generate_answer
        from debug_mode import run_debug_mode

        return run_debug_mode(query, generate_answer)

        # This block is deprecated — execution handled earlier


pass
#    chunks = []
#    task_type = classify_task(query)

#    if mode == "tool":
#        return run_tool_mode(query, chunks, task_type)

#    elif mode == "teach":
#        return teach_mode(query, ["tool_validator.py"], generate_answer)

#    elif mode == "debug":
#        return "Debug mode not implemented yet"

#    else:
#        return "Unknown mode"


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
        print("\n> (Enter command. Type END on a new line to submit)")

        lines = []
        while True:
            line = input()
            if line.strip() == "END":
                break
            lines.append(line)

        query = "\n".join(lines).strip()

        if not query:
            continue

        print(f"DEBUG RAW INPUT: [{query}]")

        mode = None
        skip_bypass = False

        # -----------------------------
        # ROUTER
        # -----------------------------
        teach_keywords = ["explain", "describe", "where", "what", "how", "why"]

        code_indicators = [".py", "function", "code", "file"]

        query_lower = query.lower()

        # -----------------------------
        # MANUAL MODE OVERRIDE (PRIORITY)
        # -----------------------------
        first_line = query.strip().split("\n")[0]

        if first_line.startswith("/debug"):
            from debug_mode import run_debug_mode

            result = run_debug_mode(query, generate_answer)
            print(result)
            continue

        elif query.startswith("/run"):
            mode = "tool"

        elif query.startswith("/teach"):
            mode = "teach"

        # -----------------------------
        # AUTO MODE DETECTION (FALLBACK)
        # -----------------------------
        elif any(word in query_lower for word in teach_keywords):
            mode = "teach"
        else:
            mode = "tool"

        print(f"DEBUG MODE: {mode}")

        # -----------------------------
        # TEACH MODE
        # -----------------------------
        if mode == "teach":
            system_files = ["tool_validator.py"]
            response = teach_mode(query, system_files, generate_answer)
            print(response)
            continue

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
            raw = query[len("/add_idea ") :].strip()

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

            has_vague = words & vague_terms
            has_action = any(
                w in words
                for w in [
                    "clean",
                    "organize",
                    "setup",
                    "fix",
                    "debug",
                    "analyze",
                    "build",
                    "create",
                    "inspect",
                    "trace",
                    "repair",
                ]
            )
            has_object = len(words) >= 2

            if has_vague or not (has_action and has_object):
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

        # -----------------------------
        # FOCUS SYSTEM (DISABLED)
        # -----------------------------
        FOCUS_ENABLED = False

        if FOCUS_ENABLED:
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
            print("DEBUG: entering tool mode")
            response_text = run_tool_mode(query, chunks, task_type)
            print("DEBUG: tool mode finished")
        #            response_text = run_tool_mode(query, chunks, task_type)
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


# -----------------------------
# TEMP: Teach Mode Test Harness
# (set to true for isolated testing)
# -----------------------------
if False:
    system_files = ["tool_validator.py"]

    user_input = input(">> ")

    response = teach_mode(user_input, system_files, generate_answer)

    print(response)
