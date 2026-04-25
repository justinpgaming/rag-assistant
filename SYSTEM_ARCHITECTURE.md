# 🧭 SYSTEM ARCHITECTURE

---

## 🧠 Core Structure

User Input
   ↓
Router
   ↓
Mode
   ↓
Mode Pipeline
   ↓
Output

---

## 🧩 Modes

### Tool Mode
- Step-by-step execution
- Strict validation
- Minecraft-focused

Pipeline:
LLM → parser → validator → correction → scoring → output

---

### Teach Mode
- Explanation + debugging
- Step-by-step reasoning
- No strict validation

---

### Fast Mode
- Direct answers
- No processing pipeline

---

## 🔌 Modularity Rules

- Each mode is standalone
- No cross-mode dependency
- Modes can be removed without breaking system

---

## 🧠 Responsibility Separation

LLM → generates  
Validator → enforces rules  
Scoring → ranks quality  

NEVER mix these roles

---

## ⚠️ Constraint Handling Rule

Logical instruction:
❌ "do not connect"

Physical instruction:
✅ "leave gap" / "place block"

---

## 🚀 Expansion Path

- Add new modes without touching existing ones
- Extend Tool Mode with Minecraft knowledge
- Introduce RAG later for domain knowledge

from here on is called the "new version"  but the format is changed so i kept the old above it just in case... too many times far too much information
was missed, not passed along, and things broke, costing hours of debugging etc.

SYSTEM: RAG TASK EXECUTION ASSISTANT

USER SKILL LEVEL:
- Beginner
- Cannot reliably infer missing steps
- Requires explicit, precise instructions
- Vague guidance WILL break the system

CORE RULE:
- Never assume the user understands implied steps
- Always give exact placement, exact code, exact changes


----------------------------------------
SYSTEM PURPOSE
----------------------------------------

Generate structured, step-by-step physical task workflows.

Then:
- Validate each step
- Correct invalid steps
- Ensure logical workflow order
- Provide clean final output

System evolves through:
- validation rules
- correction logic
- experience memory


----------------------------------------
MODES
----------------------------------------

TOOL MODE:
- Outputs final cleaned steps only
- No explanations

DEBUG MODE:
- Shows internal pipeline stages
- Used for development and troubleshooting

TEACH MODE:
- Explains what happened during THIS run
- Shows:
  - raw model output
  - validation results
  - corrections applied
  - final output
  - workflow issues
- Does NOT modify logic


----------------------------------------
PIPELINE FLOW
----------------------------------------

input
→ prompt generation
→ LLM output
→ step parsing
→ step validation
→ correction (if needed)
→ rebuild output
→ workflow check
→ final output


----------------------------------------
VALIDATION PRINCIPLES
----------------------------------------

- One step = one action
- No vague wording
- No weak verbs
- No impossible actions
- No multi-action chaining

Validation MUST NOT:
- Overcorrect
- Conflict with itself
- Duplicate logic


----------------------------------------
CORRECTION PRINCIPLES
----------------------------------------

- Fix only what is invalid
- Do not introduce new errors
- Prefer simple, physical actions
- Use controlled verb set

Correction is NOT validation


----------------------------------------
WORKFLOW PRINCIPLES
----------------------------------------

- Steps must follow logical order
- No backward actions (e.g. cleaning before pickup)
- No redundant work


----------------------------------------
CURRENT SYSTEM STATE
----------------------------------------

- Validator: being cleaned (removing rule conflicts)
- Correction: functional, improving
- Workflow checker: active
- Debug mode: being structured
- Teach mode: partially implemented


----------------------------------------
DEVELOPMENT RULES
----------------------------------------

- NEVER add duplicate validation rules
- NEVER mix validation and correction logic
- NEVER use vague instructions when modifying code
- ALWAYS specify exact insertion points
- ALWAYS test after changes


----------------------------------------
KNOWN RISKS
----------------------------------------

- Large files (~18k lines) make debugging difficult
- Copy/paste errors frequently break structure
- Small indentation errors can break execution


----------------------------------------
PRIORITY GOAL
----------------------------------------

1. Finalize DEBUG mode
2. Finalize TEACH mode
3. Then refactor and expand system