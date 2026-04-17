⚠️ ROADMAP RULE

Before making changes or discussing roadmap:

Confirm roadmap is up to date
If not → update it first
Do NOT continue until confirmed

Purpose:
Prevent loss of decisions and progress due to context switching

🧠 RAG Assistant – System Roadmap & State
🎯 CORE VISION

Build a fully offline, controlled AI assistant with:

Deterministic behavior
Task focus system
Mode-based reasoning control
Memory + retrieval (RAG)
Expandable architecture
High reliability and controllability
🏗 CURRENT ARCHITECTURE
Core Flow

User Input
→ Command Handling
→ Focus System
→ Mode System
→ (Conditional RAG)
→ Prompt Builder
→ LLM
→ Logging

🧠 SYSTEM COMPONENTS
1. RAG System
Loads local data
Embeddings via sentence-transformers
Retrieves relevant chunks
Disabled in TOOL mode (intentional)
Working correctly
2. Memory System
Stores goals + decisions
JSON-based persistence
Basic but functional
3. Focus System
Tracks current task
Detects task switching
Supports:
strict mode
guided mode
queue system
Working
4. Mode System (CRITICAL)
Modes:
fast
think
tool
Behavior:

Mode is passed into prompt builder → changes LLM output behavior

5. Prompt System
Fully separated into prompt.py
Mode-driven behavior injection
Supports task-type extension (in progress)
6. LLM Integration
Uses local Ollama (llama3)
Streaming responses
Stable
7. Logging System
Logs interactions to logs.jsonl
Functional, basic structure
🔥 MAJOR DECISIONS MADE
✅ Separation of Concerns
main.py = control + routing
focus.py = state logic
prompt.py = behavior control
llm.py = execution layer
🔒 Mode Behavior Rules (Core System Logic)
⚡ FAST MODE
Immediate answers
Minimal output
No reasoning
🧠 THINK MODE
Step-by-step reasoning
Logical structure
No filler
🛠 TOOL MODE
Deterministic step execution
Output ONLY numbered steps
No explanations
No introductions
No summaries
No assumptions unless specified
RAG is bypassed
Prioritizes action over explanation
🔑 Key Rule

Mode changes:

Prompt structure
Output format
Allowed behavior

NOT just tone

🛡 RELIABILITY LAYER (NEW — HIGH PRIORITY)
Purpose:

Transform system from probabilistic → controlled + predictable

1. Output Validation Layer (CRITICAL)
Function:
Validate LLM output before display/logging
Checks:
Starts with 1.
Contains multiple steps
No forbidden phrases (e.g., "Here is", "Below is")
No extra text outside steps
Behavior:
Reject invalid outputs
Optionally retry generation
2. Task Type Detection
Function:

Classify task before prompt building

Types:
development
physical
general (fallback)
Purpose:
Improve TOOL mode accuracy
Enable prompt specialization
3. Structured Logging Upgrade
Add fields:
mode
task_type
validation_result
response_time
Purpose:
Debugging
Behavior analysis
Performance tracking
4. Debug Control System
Add:
DEBUG = True
Behavior:
Toggle debug logs on/off
Purpose:
Clean output vs verbose debugging
5. Safety Guards (System-Level)
Add:
Max step count limit
Reject empty outputs
Reject overly short outputs
Purpose:

Prevent broken or useless responses

6. Retry Mechanism (Optional Enhancement)
Behavior:
Regenerate response if validation fails
Limited attempts (e.g., 2–3)
Purpose:

Improve reliability without manual intervention

🧭 FUTURE LAYERS (Planned, Not Active)
🖥 UI Layer
Command palette interface
Hotkey-triggered
Click-based command execution
Uses existing command system (no duplication)
🧱 NEXT DEVELOPMENT PRIORITIES
Output Validation Layer
Task Type Detection
Structured Logging Upgrade
Debug Control System
Safety Guards
Retry Mechanism
🧠 CURRENT STATE SUMMARY

System is now:

Stable
Modular
Controllable
Ready for reliability improvements

Transitioning from:

→ “working system”

to:

→ “controlled and predictable system”