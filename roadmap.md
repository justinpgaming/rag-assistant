# ⚠️ ROADMAP RULE

Before making changes or discussing roadmap:

1. Confirm roadmap is up to date
2. If not → update it first
3. Do NOT continue until confirmed

Purpose:
Prevent loss of decisions and progress due to context switching.




# 🧠 RAG Assistant – System Roadmap & State

---

# 🎯 CORE VISION

Build a fully offline, controlled AI assistant with:

- Deterministic behavior
- Task focus system
- Mode-based reasoning control
- Memory + retrieval (RAG)
- Expandable architecture

---

# 🏗 CURRENT ARCHITECTURE

## Core Flow

User Input → Command Handling → Focus System → Mode System → RAG → Prompt Builder → LLM → Logging

---

# 🧠 SYSTEM COMPONENTS

## 1. RAG System
- Loads local data
- Embeddings via sentence-transformers
- Retrieves relevant chunks
- Working correctly

---

## 2. Memory System
- Stores goals + decisions
- JSON-based persistence
- Basic but functional

---

## 3. Focus System
- Tracks current task
- Detects task switching
- Supports:
  - strict mode
  - guided mode
  - queue system

---

## 4. Mode System (CRITICAL)

### Modes:
- fast
- think
- tool

### Behavior:
Mode is passed into prompt builder → changes LLM output behavior

---

## 5. Prompt System

Moved from inline (main.py) → dedicated `prompt.py`

### Key Decision:
- FULL separation of prompt logic from main loop

---

## 6. LLM Integration

- Uses local Ollama (`llama3`)
- Streaming responses
- Stable

---

## 7. Logging System

- Logs interactions to `logs.jsonl`
- Working

---

# 🔥 MAJOR DECISIONS MADE

## ✅ Separation of Concerns

- `main.py` = control + routing
- `focus.py` = state logic
- `prompt.py` = behavior control
- `llm.py` = execution layer

---

## 🔒 Mode Behavior Rules (Core System Logic)

### ⚡ FAST MODE

- Goal: Immediate answer
- Behavior:
  - Minimal output
  - No reasoning steps
  - No breakdown

---

### 🧠 THINK MODE
- Goal: Structured reasoning
- Behavior:
  - Step-by-step breakdown
  - Clear logical flow
  - No conversational filler

---

### 🛠 TOOL MODE
- Goal: Action execution
- Behavior:
- Only output steps
- No explanations
- Be deterministic
- Must NOT assume any environment unless explicitly stated
- If the task does not explicitly mention software, code, or a computer, assume it is a real-world physical task

---

### 🔑 Key Rule

Mode selection changes:
- Prompt structure
- Output format
- Allowed behavior

NOT just tone or style.


# 🧭 FUTURE LAYERS (Planned, Not Active)

## 🖥 UI Layer (Future)

- Command palette style interface (popup / dropdown)
- NOT always visible
- Triggered on demand (hotkey or button)
- Displays available commands
- Allows click-based execution instead of typing
- Must use existing command system (no duplicated logic)