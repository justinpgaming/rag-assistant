from rag import load_data, retrieve
from llm import generate_answer
from memory import load_memory, add_goal, add_decision
from focus import handle_focus, set_task, get_task, add_to_queue, view_queue, pop_next_task
from focus import complete_task

def main():
    print("🧠 Loading RAG system...")
    
    try:
        database = load_data()
    except Exception as e:
        print(f"❌ Failed to load data: {e}")
        return

    print(f"✅ Loaded {len(database)} chunks")

    # Load memory
    memory = load_memory()
    print(f"🧠 Memory loaded: {len(memory['goals'])} goals, {len(memory['decisions'])} decisions")

    while True:
        query = input("\n> ")

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
        # FOCUS SYSTEM (GUIDED + QUEUE)
        # -----------------------------
        allowed, new_task = handle_focus(query)

        if not allowed:
            current = get_task()

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

        # Retrieve relevant chunks
        chunks = retrieve(query, database)

        # Generate answer using LLM (streaming)
        print("\n🤖 Answer:\n")

        for chunk in generate_answer(query, chunks, memory):
            print(chunk, end="", flush=True)

        print()  # final newline


if __name__ == "__main__":
    main()
