# 🧠 RAG Assistant (Work In Progress)

## 📌 What This Is
A local AI assistant built from scratch using:
- Retrieval-Augmented Generation (RAG)
- Tool-based task execution (step-by-step actions)
- Validation + correction loop for reliability

This project is focused on building a high-reliability assistant, not just a chatbot.

---

## 📊 Current Progress

- Interactive CLI (main.py)
- Tool mode (/run <task>)
- Step validation system
- Automatic correction loop
- Persistent memory:
  - Goals
  - Decisions
  - Ideas
- Basic focus system (task tracking)

---

## 🚀 How to Run

    python main.py

---

## 🧪 Testing Tool Mode

    python test_tool_mode.py

---

## 💬 Commands

    /add_goal <text>
    /add_decision <text>
    /add_idea <text>

    /view_ideas
    /view_tasks
    /view_logs

    /run <task>
    /set_mode <mode>

Modes:
- fast
- think
- tool

---

## 🧠 Project Structure

    main.py             → main control loop
    rag.py              → retrieval system
    llm.py              → model interface
    tool_validator.py   → validation + correction logic
    memory.py           → persistent memory
    focus.py            → task + mode handling
    logger.py           → logging system
    viewer.py           → log viewer
    prompt.py           → prompt construction
    test_tool_mode.py   → tool mode tests

---

## ⚠️ Important Notes

- This project is under active development
- Structure and behavior may change frequently
- Focus is on reliability and correctness, not speed or polish

---

## 🎯 Current Focus

- Improve validation accuracy
- Strengthen correction system
- Introduce workflow awareness (next phase)

---

## 🧭 Next Steps

- Add workflow detection (not enforcement)
- Improve vague wording correction
- Expand testing coverage

---

## 🧪 Philosophy

This system is being built with:

- strict validation
- controlled correction
- layered intelligence

Goal:
A trustworthy assistant capable of real-world task guidance.