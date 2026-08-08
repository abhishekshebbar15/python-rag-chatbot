import faiss
import pickle
from sentence_transformers import SentenceTransformer
import ollama


# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")


# Load FAISS index
index = faiss.read_index("vector_index/python.index")


# Load text chunks
with open("vector_index/chunks.pkl", "rb") as f:
    chunks = pickle.load(f)


def ask_rag(question):

    # Convert question into embedding
    question_embedding = model.encode([question])

    # Search FAISS
    distances, indices = index.search(question_embedding, k=3)

    # Get relevant chunks
    context = ""

    for index_number in indices[0]:
        context += chunks[index_number] + "\n\n"


    # Create prompt for Llama
    prompt = f"""
You are a Python tutor and a strict Retrieval-Augmented Generation (RAG) assistant.

IMPORTANT RULES:

1. Answer ONLY using the information provided in the CONTEXT.
2. Do NOT use your general knowledge.
3. Do NOT search for or suggest external sources.
4. Do NOT add information that is not present in the CONTEXT.
5. If the answer cannot be found in the CONTEXT, respond EXACTLY:
"Sorry, I couldn't find this information in my Python knowledge base."
6. Do not suggest Wikipedia, Google, other websites, or other resources.
7. Keep the answer clear and simple.

CONTEXT:
{context}

QUESTION:
{question}

ANSWER:
"""


    # Ask Llama
    response = ollama.chat(
        model="llama3.2",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response["message"]["content"]