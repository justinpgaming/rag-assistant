FORMAT RULE (IMPORTANT):

All new entries must start with one tag:
IDEA | BUG | DECISION | QUESTION | NOTE

Old content is untagged and ignored unless needed.

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


# 💡 Free Thinking / Future Ideas (NOT IMPLEMENTED)

This section contains ideas discussed during development that are NOT part of current architecture.

They are preserved here to avoid loss of direction.

---

## 🧠 1. Teaching Mode Expansion
- System explains its own decisions step-by-step
- Shows:
  - why a step was changed
  - why validation failed
  - correction reasoning chain

Status: future phase (after stability)

---

## 🧠 2. Diagram System (Minecraft + Debug)
- Convert validated steps into visual flow
- ASCII first version
- Later GUI-based visualization

Example:
[Furnace]
   ↓
[Hopper]
   ↓
[Chest]

Status: planned

---

## 🧠 3. Domain Expansion System
- Add new domains:
  - minecraft
  - general tasks
  - debugging workflows

Each domain has:
- own validation rules
- own correction style

Status: future architecture layer

---

## 🧠 4. Validator Decoupling (Important Insight)
- Current validator is too centralized
- Future idea:
  - split per-domain validators
  - cleaning validator ≠ debug validator

Status: planned structural upgrade

---

## 🧠 5. RAG Enhancement Layer
- Improve memory integration
- Use learned experiences to influence corrections

Status: later phase (after validator stabilizes)

Cleaning Domain:
  - validator: strict single-action rules
  - correction: simplify + split actions

Debug Domain:
  - validator: structural correctness only
  - correction: preserve logic, not simplify

Minecraft Domain:
  - validator: spatial + block legality
  - correction: adjust structure, not wording

  🧠 Clarified System Design Insight (Modes + Output Contracts)
📌 Key Understanding (Updated)

The system is not designed as multiple agents collaborating on a single answer.

Instead:

The system routes each user request to ONE mode, and that mode fully owns the response.

This was previously misunderstood as a “multi-agent assembly system”, but that design creates instability and overlapping logic.

🧱 Correct Mode Structure

Each mode is a sealed execution pipeline with a strict output contract:

🟦 Tool Mode

Purpose: Execution planning

Output:

Step-by-step instructions
Point form
Action-focused
No explanations or debugging detail

Example:

Do this
Then do this
Replace X with Y
🟥 Debug Mode

Purpose: Identify and fix code issues

Output:

Relevant code snippet
Highlighted error location
Error explanation (short)
Suggested fix

Focus: “what is broken + how to fix it”

🟨 Teach Mode

Purpose: Learning and understanding

Output:

Explanation of concept
Why it works this way
Proper usage patterns
Examples

Focus: “understanding, not fixing current code”

⚠️ Critical Rule

Modes MUST NOT overlap responsibilities.

Tool Mode does NOT explain concepts
Debug Mode does NOT teach general usage
Teach Mode does NOT provide direct patch instructions

Each mode answers only its own question type.

🧠 Design Insight

Earlier system instability was caused by:

Shared validation rules across modes
Overlapping output expectations
Implicit mixing of Teach / Debug / Tool behavior
Lack of strict output contracts per mode

This led to:

Tool Mode becoming overly strict or inconsistent
Validation false failures
Correction system instability
🧱 Core Principle (Locked In)

Each mode is a complete response system with a fixed output format, not a partial contributor to a combined answer.

There is no “assembly of multiple full answers”.

Instead:

Router selects ONE mode
That mode produces ONE final structured output
Output is formatted, not merged
🚀 Future Benefit of This Design

This separation enables:

Stable Tool Mode behavior
Predictable validation
Clear debugging workflows
Clean UI rendering (Streamlit or future GUI)
Easier expansion into new domains (e.g. Minecraft, automation)
🧭 Final Mental Model

User Input
→ Router selects mode
→ Mode runs full pipeline
→ Mode outputs final structured response
→ UI displays result (no merging layer)


🧱 Recommendation Lifecycle (Future Design)

Each suggested change follows this lifecycle:

Detection
Teach Mode identifies recurring issues:
repeated validation failures
low scoring patterns (e.g. ~70 ceiling)
structural inconsistencies
Recommendation Generation
Teach Mode outputs:
what to change
where to change it (file / prompt section)
why the change is needed
expected impact
User Decision Layer
User may:
accept
reject
modify suggestion
Implementation (Manual or Assisted)
Changes are applied manually OR via optional future “soft edit system”
Outcome Grading System
After sufficient runs, changes are evaluated:
very bad → system regression
bad → worse performance
neutral → no meaningful change
good → improvement
very good → clear improvement
History Tracking
All recommendations stored with:
before/after metrics
scoring trends
validation impact
⚠️ Safety Constraints
Tool Mode MUST remain unchanged during execution
No scoring-based live prompt modification
No automatic self-editing of core logic during runtime
All system changes must be:
logged
reversible (Git-based preferred)
reviewable
🧠 Soft Auto-Edit System (Future Consideration)

A future optional layer may allow:

minimal safe prompt edits
automatic backup creation
diff-based change logs
strict constraint on scope (non-logic changes only)

This system must:

never modify validator or Tool Mode logic directly
always preserve rollback ability
always log exact change diff
📊 Design Goal

Enable long-term system improvement via:

structured observation
delayed feedback loops
controlled human approval
reproducible system evolution
🧭 Principle

The system learns over time, but never changes itself in real time.