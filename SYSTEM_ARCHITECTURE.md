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