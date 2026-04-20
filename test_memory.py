from memory_experience import (
    load_experience_memory,
    update_memory_from_log,
    save_experience_memory,
)

memory = load_experience_memory()

fake_log = {
    "task_type": "cleaning",
    "validation": [
        {
            "text": "Straiten and arrange visible items",
            "valid": False,
            "reason": "vague wording",
        }
    ],
}

memory = update_memory_from_log(fake_log, memory)
save_experience_memory(memory)

print("✅ Memory updated")
