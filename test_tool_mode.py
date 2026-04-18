from main import run_tool_mode
from rag import load_data

TEST_TASKS = [
    "clean my room",
    "clean the kitchen",
    "organize my desk",
    "wash dishes",
    "reset my workspace",
]

def run_tests():
    database = load_data()

    for task in TEST_TASKS:
        print("\n" + "="*50)
        print(f"TEST: {task}")
        print("="*50)

        output = run_tool_mode(task, [], "cleaning")

        print("\nOUTPUT:\n")
        print(output)


if __name__ == "__main__":
    run_tests()