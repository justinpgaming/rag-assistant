🧭 SYSTEM ARCHITECTURE (CLEAN & ALIGNED)
🧠 1. Core Mental Model

This system is a:

Structured task execution engine

It:

Takes user input
Converts it into structured steps
Validates those steps
Corrects mistakes
Returns clean, usable output
🔑 Key Idea

The system is NOT “just an AI”

It is:

Controlled Pipeline + Rules + Correction + Memory
🔌 2. Entry Layer (EXTERNAL)
User → Interface (CLI / UI) → System Input
Explanation:
The interface (CLI, Streamlit, etc.) collects input
Then passes it into the system
The system starts at input

⚠️ This layer is NOT part of internal logic
⚠️ It can be changed without breaking the system

🧠 3. Input Interpretation Layer (FUTURE)
raw input → structured command
Purpose:

Convert natural language into structured system commands

Example:

Input:

fix syntax error on line 24 in validate_tool.py

Becomes:

/debug
[ERROR] syntax error
[FILE: validate_tool.py]
[LINE: 24]
END
Responsibilities:
Detect intent (debug vs task)
Extract key data (file, line, error)
Build structured command
Reject incomplete input
Status:

❌ Not implemented yet
⚠️ DO NOT build yet

🧭 4. Command Router (EXISTS)
input → command router → mode
Purpose:

Determine which mode to run

Current Behavior:
/run → Tool Mode
/debug → Debug Mode
Important:

This router:

DOES NOT understand tasks
ONLY selects execution mode
🧠 5. Domain Router (MISSING – NEXT STEP)
task → domain → correct logic
Purpose:

Ensure correct logic is applied to the correct task type

Example:
"clean room" → cleaning domain
"fix python error" → debug domain
"build redstone" → minecraft domain
Why This Is Critical:

Without this:

❌ Cleaning logic affects everything
❌ Validator rejects valid non-cleaning tasks
❌ Correction becomes incorrect

Status:

❌ Not implemented
🎯 NEXT MAJOR MILESTONE

🧩 6. Modes (HOW the system runs)

Modes control execution style, not logic.

🔧 Tool Mode (PRIMARY)
structured execution pipeline
Generates steps
Validates steps
Corrects steps
Returns final output
🐛 Debug Mode
error analysis pipeline
Parses structured debug input
Extracts file + line context
Analyzes error
📚 Teach Mode (PARTIAL)
explanation layer
Shows:
model output
validation results
corrections
Does NOT change logic
⚠️ Key Distinction
Type	Purpose
Domain	WHAT logic runs
Mode	HOW it runs
🔁 7. Tool Mode Pipeline (CURRENT CORE)
input
 → prompt generation
 → LLM output
 → step parsing
 → step validation
 → correction
 → retry loop
 → final output
Components:
1. Prompt Generator
Builds instructions for LLM
2. Step Parser
Converts text → structured steps
3. Validator
Enforces rules
Detects invalid steps
4. Correction Loop
Fixes invalid steps
Re-runs when needed
5. Retry Loop
Retries full pipeline (max 2–3)
6. Experience Memory
Logs outcomes for learning
🧪 8. Debug Mode Flow
structured debug input
 → parse fields
 → load file context
 → analyze error
 → return explanation
Input Requirements:
/debug
[ERROR] ...
[FILE: ...]
[LINE: ...]
END
Behavior:
Rejects missing fields
Does NOT guess missing data
Uses structured input only
🧱 9. System Control Flow (FULL VIEW)
User Input
 → (future) Input Interpreter
 → Command Router
     → Tool Mode
         → (future) Domain Router
             → Tool Pipeline
     → Debug Mode
         → Debug Pipeline
 → Output
⚠️ 10. Current Limitations
1. No Domain Routing
All tasks use cleaning logic
2. Validator Bias
Overfitted to cleaning domain
3. Correction Instability
Not domain-aware
4. Input Fragility
Requires structured commands manually
🎯 11. Current Development Phase
Phase 1: Pipeline Stability ✅
Phase 2: Domain Control ← CURRENT
Phase 3: Intelligence (future)
🚫 12. What NOT To Do (Right Now)
Do NOT expand validator rules
Do NOT add more retry systems
Do NOT optimize prompts
Do NOT build input interpreter yet
🎯 13. Immediate Next Step
👉 Implement Domain Router

Goal:

cleaning → cleaning logic
debug → debug logic
minecraft → future
🚀 14. Future Expansion (Controlled)
After Domain Control:
Domain-specific validators
Domain-specific correction logic
Input interpreter
Teach mode completion
RAG knowledge integration
🧠 Final Principle

The system must remain controlled before it becomes intelligent

✅ Summary

The system is:

✔ Structured
✔ Functional
✔ Stable

But:

❌ Not domain-aware
❌ Not flexible yet