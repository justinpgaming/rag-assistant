# 🧠 RAG Assistant Command Cheat Sheet

---

## 🔧 TOOL MODE

Run a task:

/run clean my room

---

## 🐞 DEBUG MODE

### Basic Debug (no code)

Use when describing a problem:

/debug my validator crashes on empty input

---

### Code Debug (IMPORTANT)

Use this exact structure:

/debug

[FILE: filename.py]

<PASTE YOUR CODE HERE>

---

### Code Debug with Error (BEST)

/debug

[FILE: filename.py]

<PASTE YOUR CODE HERE>

[ERROR]
<PASTE ERROR MESSAGE HERE>

---

## 🎓 TEACH MODE (WIP)

(Will explain what happened in last run)

---

## ⚠️ RULES

- ALWAYS use `[FILE: filename.py]`
- NEVER skip the FILE label
- Keep code cleanly pasted
- Add [ERROR] when possible

---

## 💡 TIPS

- Copy → paste → modify → run
- Do NOT type commands from memory
- Structure matters more than wording

---