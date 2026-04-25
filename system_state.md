# ⚙️ System State Snapshot

## 🧠 Core Systems

### 1. Tool Mode

* Parses user input into steps
* Validates steps
* Applies corrections if invalid
* Outputs structured workflow

STATUS: ⚠️ Needs refinement

---

### 2. Validator (`tool_validator.py`)

* Enforces:

  * single action
  * valid verb/object pairing
  * no ambiguity

KNOWN ISSUE:

* `REDUNDANT_PATTERNS` not defined → causes crash

FIX REQUIRED:
Define at top-level:

```python
REDUNDANT_PATTERNS = []
```

---

### 3. Step Correction System

* Attempts to fix invalid steps
* Uses scoring + retry

ISSUES:

* Sometimes produces unrelated outputs
* Overcorrects into nonsense actions

---

### 4. Debug Mode (`debug_mode.py`)

* Intended to:

  * analyze errors
  * provide structured fixes

CURRENT PROBLEM:

* Tool mode interferes with debug output
* Needs isolation from main pipeline

---

### 5. Focus System

* Detects task switching

STATUS:
❌ Disabled / unfinished
❌ Too sensitive
❌ Not ready for use

---

## 📊 Logging & Memory

* logs.jsonl → tracking outputs
* memory_experience.json → learning system

STATUS:
✅ Working but basic

---

## 🧨 Current Breaking Issue

```python
if valid and any(p in text_lower for p in REDUNDANT_PATTERNS):
```

ERROR:

```
NameError: REDUNDANT_PATTERNS is not defined
```

CAUSE:
Variable not declared in scope

---

## ✅ Immediate Fix Location

FILE: `tool_validator.py`
PLACE: **Top of file (outside any function)**

```python
REDUNDANT_PATTERNS = []
```

---

## 🧭 Behavior Observations

* System sometimes:

  * converts abstract tasks → physical actions
  * mixes contexts (debug vs cleaning tasks)

This indicates:
➡️ Prompt / routing confusion

---
