# 🧠 SYSTEM ARCHITECTURE (LOCKED DESIGN)

## 🔥 CORE PRINCIPLE

This system is NOT a single assistant with multiple behaviors.

It is:

ONE INTERFACE → ROUTES TO MULTIPLE SPECIALIZED SYSTEMS

---

## 🧠 CORE CONTROL MODEL (CRITICAL)

The system is NOT LLM-driven.

It follows this rule:

LLM → suggests output
SYSTEM → validates, evaluates, and decides final output

---

### CONTROL FLOW

```id="aa12bb"
LLM output
   ↓
VALIDATION (hard rules)
   ↓
EVALUATION (scoring)
   ↓
CORRECTION (if needed)
   ↓
FINAL OUTPUT
```

---

### 🔒 HARD RULE

The LLM is NEVER trusted as final output.

The system MUST:

* reject invalid outputs
* correct weak outputs
* enforce all rules deterministically

---

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


## 🧠 MEMORY DEFINITIONS

### Memory Types

* memory.py → personal/user memory (goals, ideas, decisions) *(temporary name)*
* memory_experience.py → system learning (failures, corrections)
* memory_context.py → short-term task/session memory *(future)*
* focus.py → system state (mode, active task, control flow) *(future: system_state.py)*(future)


## 🧠 SYSTEM DEFINITIONS

### 1. TOOL SYSTEM (CURRENT FOCUS)

### 🧩 DOMAIN ABSTRACTION (IMPORTANT)

The tool system is domain-agnostic.

It operates as:

ENGINE (fixed logic) + DOMAIN (rules + knowledge)

---

Examples of domains:

* cleaning
* development
* minecraft (future)
* other games (future)

---

### 🔒 RULE

Domains MUST NOT modify core logic.

They only provide:

* allowed actions (verbs)
* templates
* vocabulary rules
* knowledge (RAG)


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
