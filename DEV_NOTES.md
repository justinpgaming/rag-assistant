# 🧠 DEV NOTES — RAG Assistant

---

## 📌 Current Focus
- Stabilize Tool Mode (step generation system)
- Eliminate validation conflicts
- Ensure consistent, minimal, executable steps

---

## 🧱 System Direction (LOCKED)

The system is a **modular agent with routing**:

User → Router → Mode → Output

Modes are:
- Tool Mode (strict steps)
- Teach Mode (guidance / coding help)
- Fast Mode (quick answers)

Each mode is:
- Standalone
- Replaceable
- Independent

---

## 🎯 Tool Mode Philosophy

Steps must be:
- Single action
- Physically executable
- Minimal wording
- No fluff

---

## 🧠 Key Design Rules

- Validation = hard rules only
- Scoring = preference only (NOT validation)
- LLM = generation only
- No mixing responsibilities

---

## ⚠️ Critical Insight

DO NOT express logic like:
"do not connect to X"

ALWAYS convert to physical action:
"leave one block gap"

---

## 📌 Next Steps (Short Term)

1. Fix validator conflicts
2. Ensure correction system stability
3. Clean output consistency
4. Remove redundant / conflicting rules

---

## 🧪 Ideas to Explore (Soon)

- Tool-object compatibility system
- Redstone constraint vocabulary
- Basic router implementation

---

## 🧱 System Improvements

- Simplify validator structure
- Reduce over-rejection
- Improve correction quality
- Add debug clarity

---

## 🐞 Issues / Bugs

- Some valid steps being rejected
- Correction loop producing worse outputs
- Workflow warnings not actionable yet

---

## ⚠️ Pain Points

- Copy/paste indentation issues
- Large file complexity (~700 lines)
- Hidden rule conflicts

---

## 🧭 Decisions Made

- DO NOT overengineer early
- Keep system physically grounded
- Separate all responsibilities cleanly
- Build Tool Mode first, then expand

---

## 🚀 Future Vision

- Minecraft build system (core focus)
- Mod support (Create, Skyblock, etc)
- Teaching system for Python/Linux
- Real-time game analysis (long-term)
- Automation / assistant integration


---

## 🖥️ GUI DESIGN RULE (CRITICAL - DO NOT BREAK)

The GUI must NEVER replace or bypass the command system.

The system is command-first, GUI-second.

### ✅ REQUIRED ARCHITECTURE

GUI
→ builds command string
→ sends to main.py
→ router
→ mode

---

### ✅ EXAMPLE

If user selects Debug Mode in GUI:

The GUI MUST generate:

/debug

[FILE: example.py]

<code here>

[ERROR]
<error here>

---

### ❌ DO NOT DO THIS

- Do NOT call mode functions directly from GUI
- Do NOT pass structured arguments like:
  run_debug_mode(code, error, file_name)

- Do NOT create a separate execution path for GUI

---

### ✅ WHY THIS RULE EXISTS

- Keeps system modular
- Prevents duplicate logic
- Allows CLI and GUI to behave identically
- Prevents future debugging complexity
- Makes system easier to maintain and expand

---

### 🧠 PRINCIPLE

The GUI is ONLY a visual layer.

It does NOT contain logic.
It does NOT replace commands.
It ONLY builds and sends commands.

---