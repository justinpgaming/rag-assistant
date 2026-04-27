# 🧱 Development Rules (CRITICAL)

## ❗ Absolute Rules

1. NEVER assume user knowledge
2. ALWAYS provide:

   * file name
   * exact location
   * exact code block
3. NEVER give partial instructions
4. ALWAYS preserve indentation
5. NEVER restructure code unless explicitly requested

---

## 🧠 Teaching Style Required

* Step-by-step
* Clear reasoning
* No skipped logic
* Explain *why*, not just *what*

---

## 🔧 Code Change Rules

When modifying code:

* Show BEFORE
* Show AFTER
* Keep context small
* Do NOT reformat unrelated code

---

## ⚠️ Copy/Paste Constraints

User experiences:

* indentation breaking on paste
* needs manual tab correction

Therefore:

* Keep blocks minimal
* Avoid deeply nested examples
* Warn when indentation matters

---

## 🧪 Debugging Rules

When error appears:

1. Identify exact cause
2. Explain simply
3. Show exact fix
4. Specify file + placement
5. Provide minimal working code

---

## 🔄 Workflow Rules

* Commit before risky changes
* Test after each change
* Prefer small steps over large rewrites

---

## 🚫 Avoid

* Abstract explanations without grounding
* Large rewrites
* “just fix it like this” responses
* Hidden assumptions

---

## ✅ Preferred Style

* Structured
* Predictable
* Explicit
* Repeatable

---
 version 2.0 below, in case things were missed, this is to compare only

 # 🧱 Development Rules (STRICT)

## 🚨 Core Rule

Stability > Features

---

## 🧠 Beginner Safety Rules

* NEVER assume code works after editing
* ALWAYS test after changes
* NEVER paste partial code blocks
* ALWAYS replace full sections when instructed

---

## 📋 Editing Rules

When modifying code:

1. Copy EXACT block
2. Replace ENTIRE block
3. Do NOT merge manually
4. Keep indentation EXACT

---

## 🧪 Testing Rules

After ANY change:

1. Run program
2. Test `/run clean my room`
3. Test `/debug`
4. Confirm no crashes

---

## 🔁 Retry Logic Rule

* Only ONE retry loop allowed (tool mode)
* Max attempts = 2 or 3
* NO nested retry loops

---

## 🧠 Architecture Rules

DO NOT:

* Mix domains (cleaning, debug, minecraft)
* Add logic without routing
* Duplicate functions

---

## 🧩 File Size Rule

If file > ~2000–3000 lines:

👉 Split it

Examples:

* `tool_validator.py`
* `tool_sanity.py`
* `debug_utils.py`

---

## ⚠️ Common Mistakes

* Adding return too early (kills logic)
* Forgetting imports
* Duplicating functions
* Breaking indentation

---

## 🎯 Priority Order

1. Stability
2. Structure
3. Domain control
4. Intelligence
5. Features

---

## 🧠 Golden Rule

If something feels confusing:

👉 STOP
👉 Ask
👉 Do NOT guess

---

## 📌 Summary

This system must remain:

* Predictable
* Structured
* Easy to debug

NOT:

* Smart but unstable
