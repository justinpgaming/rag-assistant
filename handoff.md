# 🧠 RAG Assistant – Clean Handoff

## 📍 Current State

The system is functional and stable at a **pipeline level**, with the following working:

* Command system (`/run`, `/debug`)
* Tool mode pipeline:

  * Prompt generation
  * Step parsing
  * Step validation
  * Correction loop
  * Experience memory logging
* Debug mode:

  * Structured error parsing (partial)
  * Context extraction (working)
* Retry loop (NEW)
* System runs end-to-end without crashing (after stub fixes)

---

## ⚠️ Known Issues (IMPORTANT)

1. **Domain Mixing (CRITICAL)**

   * Cleaning logic is being applied to ALL tasks
   * Example: debug tasks become "wipe logs", "pick up trash"
   * This is the NEXT major fix

2. **Sanity Check Not Implemented**

   * `sanity_check_tool_output()` currently stubbed or missing

3. **Validator Overfitting**

   * Current validator is tuned for cleaning tasks only
   * Causes most non-cleaning tasks to fail validation

4. **Step Correction Instability**

   * Corrections sometimes worsen output
   * Not yet domain-aware

---

## ✅ What WAS Just Completed

* Retry loop added to tool mode (outer loop, max 2–3 attempts)
* Debug mode upgraded with structured parsing
* Removed duplicate `run_tool_mode` definition
* Identified need for domain separation

---

## 🚫 DO NOT DO NEXT

* Do NOT build step-level retry yet
* Do NOT expand validator rules yet
* Do NOT optimize prompts yet

---

## 🎯 NEXT GOAL (VERY IMPORTANT)

### 👉 Implement DOMAIN CONTROL

Goal:

```
cleaning → cleaning validator
debug → debug logic
minecraft → (future)
```

This prevents cross-domain corruption.

---

## 🧠 Developer Constraints (VERY IMPORTANT)

This system is built by a beginner. Therefore:

* Instructions MUST be:

  * Explicit
  * Step-by-step
  * Copy-paste safe
* NO vague directions
* NO assumptions about prior knowledge
* ALL file edits must be clearly stated

---

## 💻 Environment

* OS: CachyOS (Linux)
* Shell: fish
* Editor: VS Code
* Known issues:

  * Copy/paste can break indentation
  * Terminal commands must be exact

---

## 🧪 How to Test System

### Run tool mode:

```
/run clean my room
```

### Run debug mode:

```
/debug
[ERROR] test
END
```

### Expected behavior:

* Tool mode runs full pipeline
* Debug mode analyzes error
* Retry loop triggers on failure

---

## 🧠 Mental Model

System is currently in:

```
Phase 1: Pipeline Stability ✅
Phase 2: Domain Separation ← NEXT
Phase 3: Step Intelligence (future)
```

---

## 🛑 If System Breaks

Check:

1. Missing imports
2. Duplicate functions
3. Early `return` killing logic
4. Indentation errors

---

## 📌 Summary

The system works.

It is NOT smart yet.

Next step is NOT more features.

Next step is:
👉 **control what logic applies to what task**


🧠 RAG Assistant — Clean System Handoff
📌 1. Current Status (Where we are now)

You are building a RAG-based step processing + correction system with the following pipeline:

Input → Parser → Validator → Correction → Scoring → Output → (optional Memory)
What is already working:
Steps are successfully parsed into structured format
Validator correctly detects:
multiple actions
weak verbs
valid atomic steps
Correction system is being triggered for invalid steps
Debug output is now visible and stable
Retry logic exists for failed corrections
⚠️ 2. Current Problems (recent issues found)
❌ A. Invalid steps sometimes pass through unchanged
Correction returns the same text
Pipeline accepts it anyway
❌ B. Duplicate outputs appear

Example:

Pick up clothes from the floor
Pick up clothes from the floor

Cause:

fallback logic reuses previous valid step
no duplicate guard
❌ C. Weak correction enforcement
“Clean the desk” is still accepted too easily
scoring overrides structural validity in some cases
❌ D. Pipeline logic confusion
invalid → corrected → still invalid → accepted anyway
retry does not guarantee structural improvement
🎯 3. Core System Goal (Important)

Your system is NOT just rewriting text.

It is enforcing:

Single atomic physical action per step

Rules:

1 action only
1 verb only (strict verb whitelist)
no combined actions
no vague objects
must remain physically executable
🧱 4. Intended Pipeline (Clean Version)
STEP 1 — Input

Raw natural language steps

STEP 2 — Parser

Converts input into:

{"index": 1, "text": "..."}
STEP 3 — Validator (TRUTH SOURCE)

Outputs:

{
  "valid": True/False,
  "reason": "...",
  "needs_decomposition": True/False
}

Rules:

Validator is FINAL authority on structure
Scoring must NOT override validator
STEP 4 — Correction (ONLY IF invalid)

Input:

step_text
reason

Output:

corrected atomic step

Rules:

MUST change invalid structure
MUST not return identical text
MUST reduce multi-action → first atomic action
MUST fix weak verb if possible
STEP 5 — Re-validation (critical)

Corrected step is re-checked

If still invalid:

retry once OR fallback atomic rewrite
STEP 6 — Final Output Assembly

Rules:

preserve order
no duplicates
no reuse of previous outputs
STEP 7 — Memory (optional future layer)

Stores:

common corrections
recurring invalid patterns
improvements for prompt refinement
🔧 5. Hard Fix Rules (Must implement next)
🚨 Rule 1: No invalid output can pass through

If:

fixed_eval["valid"] == False

Then:

final MUST NOT equal fixed
🚨 Rule 2: No unchanged corrections allowed

If:

fixed == original

→ MUST retry or regenerate

🚨 Rule 3: No duplicates allowed

Before appending:

if final in corrected:
    reject or regenerate
🧍‍♂️ 6. User Environment Constraints (IMPORTANT)

These affect how instructions must be written:

🧠 User skill level:
Beginner programmer
Needs explicit instructions
Cannot safely infer missing steps
💻 Environment:
OS: CashyOS (Arch-based Linux)
Shell: fish shell (NOT bash)
Editor: VS Code
⚠️ User limitations:
Copy/paste sometimes breaks indentation
Small formatting errors can break code
Needs exact placement instructions
📌 7. Working Style Requirements

When giving instructions:

MUST:
give exact file names
give exact function names
give exact insertion location
provide full code blocks when modifying functions
avoid assumptions
NEVER:
say “just add it somewhere”
assume bash syntax
assume standard Linux shell behavior
assume prior context not shown
🎯 8. Current System Goal (Next Milestone)

You are now stabilizing:

Correctness-first deterministic correction pipeline

Next goals:

Phase 1 (current)
fix invalid-pass-through bug
fix duplicate bug
enforce correction mutation rule
Phase 2
improve decomposition handling
introduce atomic action splitting
refine weak verb correction mapping
Phase 3
memory-based correction learning
pattern reuse optimization
🧠 9. Key Insight About Recent Issue

Your system currently behaves like:

“correction is advisory, not enforced”

It must become:

“correction is mandatory unless validator confirms fix”

📍 10. What to do next (simple action list)
Fix invalid bypass condition
Add no-change detection in correction
Add duplicate prevention before append
Ensure validator always overrides scoring
