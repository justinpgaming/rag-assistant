import os
import re
import json
import requests
import numpy as np
from sentence_transformers import SentenceTransformer


# -------- Files --------
MEMORY_FILE = "memory.json"
KNOWLEDGE_FILE = "learned_knowledge.json"


# -------- Memory --------
def load_memory():
    if not os.path.exists(MEMORY_FILE):
        return {"goals": [], "decisions": [], "system_state": {}}
    with open(MEMORY_FILE, "r") as f:
        return json.load(f)


def save_memory(memory):
    with open(MEMORY_FILE, "w") as f:
        json.dump(memory, f, indent=2)


def add_goal(goal):
    memory = load_memory()
    if goal not in memory["goals"]:
        memory["goals"].append(goal)
        save_memory(memory)


def add_decision(decision):
    memory = load_memory()
    if decision not in memory["decisions"]:
        memory["decisions"].append(decision)
        save_memory(memory)


def remove_goal(goal):
    memory = load_memory()
    matches = [g for g in memory["goals"] if goal.lower() in g.lower()]

    if not matches:
        print("⚠ No matching goal found")
        return

    if len(matches) == 1:
        memory["goals"].remove(matches[0])
        save_memory(memory)
        print(f"🗑 Goal removed: {matches[0]}")
        return

    print("\n⚠ Multiple matches found:")
    for i, m in enumerate(matches):
        print(f"{i+1}) {m}")

    choice = input("Select number to remove: ")
    if choice.isdigit():
        idx = int(choice) - 1
        if 0 <= idx < len(matches):
            memory["goals"].remove(matches[idx])
            save_memory(memory)
            print(f"🗑 Goal removed: {matches[idx]}")


def remove_decision(decision):
    memory = load_memory()
    matches = [d for d in memory["decisions"] if decision.lower() in d.lower()]

    if not matches:
        print("⚠ No matching decision found")
        return

    if len(matches) == 1:
        memory["decisions"].remove(matches[0])
        save_memory(memory)
        print(f"🗑 Decision removed: {matches[0]}")
        return

    print("\n⚠ Multiple matches found:")
    for i, m in enumerate(matches):
        print(f"{i+1}) {m}")

    choice = input("Select number to remove: ")
    if choice.isdigit():
        idx = int(choice) - 1
        if 0 <= idx < len(matches):
            memory["decisions"].remove(matches[idx])
            save_memory(memory)
            print(f"🗑 Decision removed: {matches[idx]}")


def clear_goals():
    memory = load_memory()
    memory["goals"] = []
    save_memory(memory)


def clear_decisions():
    memory = load_memory()
    memory["decisions"] = []
    save_memory(memory)


# -------- Knowledge Persistence --------
def load_knowledge():
    if not os.path.exists(KNOWLEDGE_FILE):
        return []
    try:
        with open(KNOWLEDGE_FILE, "r") as f:
            return json.load(f)
    except:
        return []


def save_knowledge(chunks):
    clean = []
    for c in chunks:
        clean.append({
            "content": c["content"],
            "metadata": c["metadata"]
        })
    with open(KNOWLEDGE_FILE, "w") as f:
        json.dump(clean, f, indent=2)


# -------- Model --------
model = SentenceTransformer('all-MiniLM-L6-v2')


# -------- Document Loader --------
def load_text_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        text = f.read()
    return {"text": text, "metadata": {"source": filepath}}


def load_all_documents(folder="data"):
    docs = []
    if not os.path.exists(folder):
        return docs
    for filename in os.listdir(folder):
        if filename.endswith(".txt"):
            docs.append(load_text_file(os.path.join(folder, filename)))
    return docs


# -------- Chunker --------
def chunk_document(document, chunk_size=300):
    text = document["text"]
    sentences = re.split(r'(?<=[.!?]) +', text)

    chunks, current = [], ""
    chunk_id = 0

    for s in sentences:
        if len(current) + len(s) < chunk_size:
            current += s + " "
        else:
            chunks.append({
                "content": current.strip(),
                "metadata": {"source": document["metadata"]["source"], "chunk_id": chunk_id}
            })
            chunk_id += 1
            current = s + " "

    if current:
        chunks.append({
            "content": current.strip(),
            "metadata": {"source": document["metadata"]["source"], "chunk_id": chunk_id}
        })

    return chunks


# -------- Embedding --------
def store_chunks(chunks):
    for c in chunks:
        c["embedding"] = model.encode(c["content"])
    return chunks


# -------- Retrieval --------
def retrieve_chunks(query, database, top_k=3):
    q_emb = model.encode(query)

    memory = load_memory()
    goals = " ".join(memory["goals"]) if memory["goals"] else ""
    g_emb = model.encode(goals) if goals else None

    scored = []

    for c in database:
        ce = c["embedding"]

        q_score = np.dot(q_emb, ce) / (np.linalg.norm(q_emb) * np.linalg.norm(ce))
        g_score = 0

        if g_emb is not None:
            g_score = np.dot(g_emb, ce) / (np.linalg.norm(g_emb) * np.linalg.norm(ce))

        final = q_score + (0.5 * g_score)
        scored.append((final, c, q_score))

    scored.sort(key=lambda x: x[0], reverse=True)

    filtered = [c for s, c, _ in scored if s > 0.25]

    if not filtered:
        fallback = sorted(scored, key=lambda x: x[2], reverse=True)
        return [c for _, c, _ in fallback[:top_k]]

    return filtered[:top_k]


# -------- Query Processing --------
def detect_procedural_query(query):
    return any(t in query.lower() for t in ["how", "how to", "steps", "process"])


def detect_multiple_topics(query):
    q = query.lower()
    for f in ["explain", "tell me about", "what are", "how do"]:
        q = q.replace(f, "")
    for sep in [" and ", " also ", " plus "]:
        q = q.replace(sep, ",")
    parts = [p.strip() for p in q.split(",") if len(p.strip()) > 2]
    return parts if len(parts) > 1 else None


# -------- Commands --------
def detect_command(query):
    q = query.lower().strip()

    if q.startswith("add goal:"): return "add_goal"
    if q.startswith("add decision:"): return "add_decision"
    if q.startswith("remove goal:"): return "remove_goal"
    if q.startswith("remove decision:"): return "remove_decision"
    if q.startswith("learn:"): return "learn"

    if q in ["goals", "show goals"]: return "show_goals"
    if q in ["decisions", "show decisions"]: return "show_decisions"
    if q == "clear goals": return "clear_goals"
    if q == "clear decisions": return "clear_decisions"

    return None


def handle_command(command, query, database):
    if command == "add_goal":
        goal = query.split(":", 1)[1].strip()
        add_goal(goal)
        print(f"✅ Goal added: {goal}")
        return True

    if command == "add_decision":
        decision = query.split(":", 1)[1].strip()
        add_decision(decision)
        print(f"✅ Decision added: {decision}")
        return True

    if command == "show_goals":
        m = load_memory()
        print("\n📌 Goals:")
        print("\n".join(f"- {g}" for g in m["goals"]) or "(none)")
        return True

    if command == "show_decisions":
        m = load_memory()
        print("\n📌 Decisions:")
        print("\n".join(f"- {d}" for d in m["decisions"]) or "(none)")
        return True

    if command == "remove_goal":
        remove_goal(query.split(":", 1)[1].strip())
        return True

    if command == "remove_decision":
        remove_decision(query.split(":", 1)[1].strip())
        return True

    if command == "clear_goals":
        clear_goals()
        print("🧹 All goals cleared")
        return True

    if command == "clear_decisions":
        clear_decisions()
        print("🧹 All decisions cleared")
        return True

    if command == "learn":
        topic = query.split(":", 1)[1].strip()
        domain = input("Enter domain (e.g. minecraft, general): ").strip().lower() or "general"

        print(f"\n🔍 Searching for: {topic}")

        try:
            search_query = f"{domain} {topic}" if domain != "general" else topic

            search_url = "https://en.wikipedia.org/w/api.php"
            params = {
                "action": "query",
                "list": "search",
                "srsearch": search_query,
                "format": "json"
            }

            response = requests.get(search_url, params=params)
            data = response.json()

            if not data["query"]["search"]:
                print("⚠ No search results found.")
                return True

            best_title = data["query"]["search"][0]["title"]

            summary_url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{best_title.replace(' ', '_')}"

            response = requests.get(
                summary_url,
                headers={"User-Agent": "rag-assistant/1.0"}
            )

            if response.status_code != 200:
                print(f"⚠ Failed to fetch summary: {response.status_code}")
                return True

            data = response.json()

            if "extract" not in data or not data["extract"]:
                print("⚠ No usable content found.")
                return True

            content = data["extract"]

            print("\n📄 Preview:\n")
            print(content[:500] + "...")

        except Exception as e:
            print(f"⚠ Failed to fetch data: {e}")
            return True

        if input("\nApprove ingestion? (y/n): ").lower() != "y":
            print("❌ Cancelled")
            return True

        doc = {
            "text": content,
            "metadata": {
                "source": f"wiki:{topic}",
                "domain": domain
            }
        }

        new_chunks = store_chunks(chunk_document(doc))
        database.extend(new_chunks)

        existing = load_knowledge()
        for c in new_chunks:
            existing.append({
                "content": c["content"],
                "metadata": c["metadata"]
            })
        save_knowledge(existing)

        print(f"✅ Learned: {topic}")
        return True

    return False


# -------- Main --------

def save_embeddings_and_chunks(database):
    embeddings = np.array([c["embedding"] for c in database])
    texts = [c["content"] for c in database]

    np.save("embeddings.npy", embeddings)

    with open("chunks.json", "w", encoding="utf-8") as f:
        json.dump(texts, f, indent=2)

    print(f"\n💾 Saved {len(texts)} chunks + embeddings")

if __name__ == "__main__":
    docs = load_all_documents()
    database = store_chunks([c for d in docs for c in chunk_document(d)])

    # Load saved knowledge
    saved = load_knowledge()
    print(f"DEBUG: loaded {len(saved)} saved chunks")

    if saved:
        print(f"\n📦 Loading {len(saved)} learned chunks...")
        saved = store_chunks(saved)
        database.extend(saved)

    save_embeddings_and_chunks(database)

    while True:
        query = input("\nAsk something (or type 'exit'): ")
        if query.lower() == "exit":
            break

        cmd = detect_command(query)
        if cmd and handle_command(cmd, query, database):
            continue

        if detect_procedural_query(query):
            print("\n⚠ Procedural question not supported.\n")
            continue

        multi = detect_multiple_topics(query)
        if multi:
            print("\n⚠ Multiple topics detected:")
            for i, t in enumerate(multi):
                print(f"{chr(65+i)}) {t}")
            continue

        results = retrieve_chunks(query, database)

        if not results:
            print("\n⚠ No relevant info found.\n")
            continue

        print("\nRetrieved Chunks:")
        for r in results:
            print(r["content"])
