## 📎 REFERENCE

For system structure and memory definitions, see:
SYSTEM_ARCHITECTURE.md

This audit focuses only on validation and verification rules.

# 🧪 SYSTEM AUDIT PLAN

---

## 🎯 Purpose

Ensure system remains:
- Stable
- Consistent
- Aligned with design rules

---

## 🔍 What to Check

### Tool Mode

- All steps are single action
- No "and" in steps
- No vague objects
- No logical instructions
- Steps are physically executable

---

### Validator

- No conflicting rules
- No duplicate logic
- Only hard validation (no scoring influence)

---

### Correction System

- Improves step quality
- Does not introduce worse outputs
- Does not loop endlessly

---

### Scoring

- Only compares quality
- Never blocks valid steps

---

## ⚠️ Red Flags

- Valid steps being rejected
- Output becoming less natural
- Increasing correction loops
- Conflicting validation reasons

---

## 🔁 Audit Frequency

- After major changes
- After rule additions
- Before expanding system

---

## ✅ Goal

Keep system:
- Predictable
- Debuggable
- Expandable