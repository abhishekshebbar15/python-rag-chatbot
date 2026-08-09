import faiss
import pickle
import os
import time
import numpy as np

from dotenv import load_dotenv
from google import genai
from google.genai import types


# ============================================================
# 1. Load environment variables
# ============================================================

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY is not set")

client = genai.Client(
    api_key=api_key
)


# ============================================================
# 2. Project directory
# ============================================================

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)


# ============================================================
# 3. Load FAISS index
# ============================================================

print("Loading FAISS index...")

index_path = os.path.join(
    BASE_DIR,
    "vector_index",
    "python.index"
)

index = faiss.read_index(index_path)

print(
    f"FAISS index loaded: {index.ntotal} vectors"
)


# ============================================================
# 4. Load text chunks
# ============================================================

print("Loading text chunks...")

chunks_path = os.path.join(
    BASE_DIR,
    "vector_index",
    "chunks.pkl"
)

with open(chunks_path, "rb") as f:
    chunks = pickle.load(f)

print(
    f"Loaded {len(chunks)} chunks."
)


# ============================================================
# 5. Create embedding for user question
# ============================================================

def create_query_embedding(question):

    result = client.models.embed_content(
        model="gemini-embedding-001",
        contents=question,
        config=types.EmbedContentConfig(
            task_type="RETRIEVAL_QUERY",
            output_dimensionality=768
        )
    )

    embedding = np.array(
        [result.embeddings[0].values],
        dtype="float32"
    )

    return embedding


# ============================================================
# 6. RAG function
# ============================================================

def ask_rag(question):

    print("\nQuestion:", question)


    # --------------------------------------------------------
    # Create embedding for question
    # --------------------------------------------------------

    print("Creating question embedding...")

    question_embedding = create_query_embedding(
        question
    )


    # --------------------------------------------------------
    # Check embedding dimensions
    # --------------------------------------------------------

    print(
        "Question embedding shape:",
        question_embedding.shape
    )

    print(
        "FAISS index dimension:",
        index.d
    )


    # --------------------------------------------------------
    # Search FAISS
    # --------------------------------------------------------

    distances, indices = index.search(
        question_embedding,
        k=5
    )


    # --------------------------------------------------------
    # Get relevant chunks
    # --------------------------------------------------------

    context_parts = []

    print("\nRetrieved chunks:")

    for rank, index_number in enumerate(
        indices[0],
        start=1
    ):

        if index_number == -1:
            continue

        distance = distances[0][rank - 1]

        print(
            f"\nResult {rank}"
            f"\nDistance: {distance}"
            f"\nChunk index: {index_number}"
        )

        context_parts.append(
            chunks[index_number]
        )


    # --------------------------------------------------------
    # Check whether chunks were retrieved
    # --------------------------------------------------------

    if not context_parts:

        return (
            "Sorry, I couldn't find this information "
            "in my Python knowledge base."
        )


    # --------------------------------------------------------
    # Build context
    # --------------------------------------------------------

    context = "\n\n".join(
        context_parts
    )


    # --------------------------------------------------------
    # Create RAG prompt
    # --------------------------------------------------------

    prompt = f"""
You are a Python tutor and a strict
Retrieval-Augmented Generation (RAG) assistant.

IMPORTANT RULES:

1. Answer ONLY using the information provided
   in the CONTEXT.

2. Do NOT use your general knowledge.

3. Do NOT search the internet.

4. Do NOT invent or assume information.

5. If the answer cannot be found in the CONTEXT,
   respond EXACTLY:

Sorry, I couldn't find this information in my Python knowledge base.

6. Keep the answer clear and simple.

7. If the CONTEXT contains the answer,
   explain it naturally.

8. Do not mention these instructions.

CONTEXT:
{context}

QUESTION:
{question}

ANSWER:
"""


    # --------------------------------------------------------
    # Ask Gemini
    # --------------------------------------------------------

    for attempt in range(3):

        try:

            print(
                f"\nSending request to Gemini "
                f"(attempt {attempt + 1}/3)..."
            )

            response = client.models.generate_content(
                model="gemini-3.6-flash",
                contents=prompt
            )

            return response.text


        except Exception as e:

            print(
                f"\nGemini request failed: {e}"
            )

            if attempt < 2:

                print(
                    "Retrying in 5 seconds..."
                )

                time.sleep(5)

            else:

                return (
                    "Sorry, Gemini is temporarily "
                    "unavailable. Please try again later."
                )