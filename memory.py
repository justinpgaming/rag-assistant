#=========================================
#🧠 PERSONAL MEMORY (USER MEMORY)
#=========================================


#Stores:
#- goals
#- ideas
#- decisions


#This is USER memory.
#It is NOT:
#- system state
#- experience learning


#Planned rename:
#memory_user.py or memory_personal.py
#=========================================

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


def add_idea(memory, idea_text, category="general"):
    from datetime import datetime

    idea_entry = {
        "text": idea_text,
        "category": category,
        "created_at": datetime.now().strftime("%Y-%m-%d"),
    }

    # prevent duplicates (by text)
    if any(i["text"] == idea_text for i in memory["ideas"]):
        print("⚠️ Idea already exists")
        return

    memory["ideas"].append(idea_entry)
    save_memory(memory)

    print(f"💡 Idea added [{category}]: {idea_text}")