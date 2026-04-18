import json
import os

MEMORY_FILE = "memory.json"

def load_memory():
    default_memory = {
        "goals": [],
        "decisions": [],
        "ideas": [],
        "tasks": [],
        "system_state": {}
    }

    # If file doesn't exist → return fresh memory
    if not os.path.exists(MEMORY_FILE):
        return default_memory

    try:
        with open(MEMORY_FILE, "r") as f:
            memory = json.load(f)

        # ✅ Ensure all keys exist (THIS is what you were missing)
        for key, value in default_memory.items():
            if key not in memory:
                memory[key] = value

        return memory

    except Exception:
        return default_memory


def save_memory(memory):
    try:
        with open(MEMORY_FILE, "w") as f:
            json.dump(memory, f, indent=2)
    except Exception as e:
        print(f"❌ Failed to save memory: {e}")


def add_goal(memory, goal):
    if goal not in memory["goals"]:
        memory["goals"].append(goal)
        save_memory(memory)
        print(f"✅ Goal added: {goal}")
    else:
        print("⚠️ Goal already exists")


def add_decision(memory, decision):
    if decision not in memory["decisions"]:
        memory["decisions"].append(decision)
        save_memory(memory)
        print(f"✅ Decision added: {decision}")
    else:
        print("⚠️ Decision already exists")


def add_idea(memory, idea):
    if idea not in memory["ideas"]:
        memory["ideas"].append(idea)
        save_memory(memory)
        print(f"💡 Idea added: {idea}")
    else:
        print("⚠️ Idea already exists")