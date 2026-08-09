import pymupdf
import faiss
import pickle
import os
import time
import numpy as np

from dotenv import load_dotenv
from google import genai
from google.genai import types


load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


# -----------------------------
# 1. Open PDF
# -----------------------------

pdf_path = "PDFs/pythonpdfcomplete.pdf"

doc = pymupdf.open(pdf_path)


# -----------------------------
# 2. Extract text
# -----------------------------

text = ""

for page in doc:
    text += page.get_text()

print("Total characters:", len(text))


# -----------------------------
# 3. Split into chunks
# -----------------------------

chunk_size = 1000

chunks = []

for i in range(0, len(text), chunk_size):
    chunks.append(text[i:i + chunk_size])

print("Total chunks:", len(chunks))


# -----------------------------
# 4. Create embeddings
# -----------------------------

all_embeddings = []

batch_size = 5

for i in range(0, len(chunks), batch_size):

    batch = chunks[i:i + batch_size]

    while True:

        try:

            print(
                f"Embedding chunks {i} to "
                f"{i + len(batch) - 1}..."
            )

            result = client.models.embed_content(
                model="gemini-embedding-001",
                contents=batch,
                config=types.EmbedContentConfig(
                    task_type="RETRIEVAL_DOCUMENT",
                    output_dimensionality=768
                )
            )

            batch_embeddings = [
                embedding.values
                for embedding in result.embeddings
            ]

            all_embeddings.extend(batch_embeddings)

            print("Batch completed!")

            # Slow down requests
            time.sleep(5)

            break

        except Exception as e:

            error = str(e)

            if "429" in error or "RESOURCE_EXHAUSTED" in error:

                print("Quota limit reached.")
                print("Waiting 30 seconds...")
                time.sleep(30)

            else:

                raise e


# -----------------------------
# 5. Convert embeddings
# -----------------------------

embeddings = np.array(
    all_embeddings,
    dtype="float32"
)

print(
    "Embedding shape:",
    embeddings.shape
)


# -----------------------------
# 6. Create FAISS index
# -----------------------------

dimension = embeddings.shape[1]

index = faiss.IndexFlatL2(dimension)

index.add(embeddings)

print(
    "Vectors stored in FAISS:",
    index.ntotal
)


# -----------------------------
# 7. Save FAISS index
# -----------------------------

os.makedirs(
    "vector_index",
    exist_ok=True
)

faiss.write_index(
    index,
    "vector_index/python.index"
)


# -----------------------------
# 8. Save chunks
# -----------------------------

with open(
    "vector_index/chunks.pkl",
    "wb"
) as f:

    pickle.dump(chunks, f)


print("FAISS index and chunks saved successfully!")