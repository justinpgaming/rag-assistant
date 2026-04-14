from rag import load_data, retrieve
from llm import generate_answer

def main():
    print("🧠 Loading RAG system...")
    
    try:
        database = load_data()
    except Exception as e:
        print(f"❌ Failed to load data: {e}")
        return

    print(f"✅ Loaded {len(database)} chunks")

    while True:
        query = input("\n> ")

        if query.lower() == "exit":
            break

        if not query.strip():
            continue

        # Retrieve relevant chunks
        chunks = retrieve(query, database)

        # Generate answer using LLM
        answer = generate_answer(query, chunks)

        print("\n🤖 Answer:\n")
        print(answer)


if __name__ == "__main__":
    main()
