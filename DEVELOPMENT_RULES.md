# 🧠 SYSTEM ARCHITECTURE (LOCKED DESIGN)

## 🔥 CORE PRINCIPLE

This system is NOT a single assistant with multiple behaviors.

It is:

ONE INTERFACE → ROUTES TO MULTIPLE SPECIALIZED SYSTEMS

---

## 🧠 CONTROL RULES (CRITICAL)

The system must always control the LLM.

---

### RULE 1: LLM IS NOT TRUSTED

* Never accept raw LLM output as final
* Always pass through validation + evaluation

---

### RULE 2: SYSTEM DECIDES FINAL OUTPUT

* LLM generates candidates
* System enforces correctness
* System chooses final result

---

### RULE 3: NO BYPASSING PIPELINE

The following pipeline is mandatory:

generate → validate → evaluate → correct → rebuild

No step may be skipped.

---

### RULE 4: WEAK MODELS MUST STILL WORK

The system must be strong enough that:

* even a weak LLM produces acceptable output

If output quality depends on model strength, the system is too weak.


## 🧩 HIGH-LEVEL ARCHITECTURE

```
MAIN INTERFACE (CLI)
        │
        ▼
   TASK ROUTER
(classify + decide)
        │
 ┌──────┼────────┬────────┐
 ▼      ▼        ▼        ▼
TOOL   TEACH    THINK    (future systems)
SYSTEM SYSTEM   SYSTEM
```

---

## 🧠 SYSTEM DEFINITIONS

### 1. TOOL SYSTEM (CURRENT FOCUS)

Purpose:

* Execute real-world tasks
* Produce structured step-by-step output

Characteristics:

* Strict rules
* Validation enforced
* Correction system active
* Scoring system (evaluate_step)

Pipeline:
LLM → validate → evaluate → correct → rebuild → output

---

### 2. TEACH SYSTEM (PLANNED)

Purpose:

* Explain system behavior
* Guide development
* Analyze failures

Characteristics:

* Reads system state (files, logs, memory)
* Not bound by strict step formatting
* Focused on clarity + guidance

Pipeline:
system data → analyze → LLM explanation → output

---

### 3. THINK SYSTEM

Purpose:

* General reasoning
* Problem solving
* Concept explanation

Characteristics:

* Step breakdowns allowed
* No strict validation
* Flexible output

---

## 🔥 CRITICAL DESIGN RULE

Modes are NOT just prompt changes.

Modes determine WHICH SYSTEM runs.

### DOMAIN RULES

Domains must be configurable, not hardcoded.

DO:

* define domain-specific verbs
* define domain templates
* plug in knowledge sources

DO NOT:

* modify core validation logic
* create domain-specific pipelines


---

## 🧠 MEMORY SEPARATION (MANDATORY)

### memory.json

Represents:

* User goals
* Ideas
* Decisions

Meaning:
WHAT THE USER KNOWS / WANTS

---

### memory_experience.json

Represents:

* Failures
* Corrections
* Scores
* Patterns

Meaning:
HOW THE SYSTEM LEARNS

---

## ⚠️ NEVER MIX THESE

memory ≠ experience_memory

---

## 🔧 CURRENT IMPLEMENTATION STATE

✔ Tool system active
✔ Validation system built
✔ Correction system in progress
✔ Evaluation system being integrated

---

## 🚀 FUTURE EXPANSION PLAN

Phase 1:

* Finalize tool system (strict + reliable)

Phase 2:

* Extract tool system into module

Phase 3:

* Implement router

Phase 4:

* Build teach system separately

---

## 🧠 FINAL MENTAL MODEL

memory = WHAT I KNOW
experience_memory = HOW I LEARN

mode = WHICH SYSTEM RUNS
NOT how one system behaves
