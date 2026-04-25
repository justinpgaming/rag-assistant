# 🧠 RAG Assistant Command Cheat Sheet

---

## 🔧 TOOL MODE

Run a task:

/run clean my room
END

---

## 🐞 DEBUG MODE

### ⚠️ REQUIRED STRUCTURE

Command MUST be first line.
END is REQUIRED.

---

### Basic Debug (structured)

Use when you have an error:

/debug
[ERROR] your error message here
END

---

### Debug with File (recommended)

/debug
[ERROR] your error message here
[FILE: filename.py]
END

---

### Debug with File + Line (BEST)

/debug
[ERROR] your error message here
[FILE: filename.py]
[LINE: 42]
END

---

### ⚠️ Code Debug (Optional)

Only use when debugging code NOT in your system files:

/debug
[FILE: temp_code.py]

<PASTE CODE HERE>

[ERROR] your error message
END

---

## 🎓 TEACH MODE (WIP)

/teach
END

---

## ⚠️ RULES

* Command MUST be first line
* ALWAYS end input with `END`
* `[ERROR]` is strongly recommended
* `[FILE: filename.py]` is optional but helpful
* `[LINE: number]` improves accuracy
* Do NOT put anything before `/debug`, `/run`, etc.

---

## 💡 TIPS

* Copy → paste → modify → run
* Do NOT type commands from memory
* Structure matters more than wording
* If something fails, check command is on first line

---
