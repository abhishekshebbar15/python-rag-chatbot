import pymupdf
from sentence_transformers import SentenceTransformer
import faiss
import pickle
import os

pdf_path = "PDFs/pythonpdfcomplete.pdf"

# 1. Open PDF
doc = pymupdf.open(pdf_path)

# 2. Extract text
text = ""

for page in doc:
    text += page.get_text()

# 3. Split text into chunks
chunk_size = 1000
chunks = []

for i in range(0, len(text), chunk_size):
    chunks.append(text[i:i + chunk_size])

print("Total characters:", len(text))
print("Total chunks:", len(chunks))

# 4. Create embeddings
model = SentenceTransformer("all-MiniLM-L6-v2")
embeddings = model.encode(chunks)

print("Embedding shape:", embeddings.shape)

# 5. Create FAISS index
dimension = embeddings.shape[1]

index = faiss.IndexFlatL2(dimension)

index.add(embeddings)

print("Vectors stored in FAISS:", index.ntotal)

# 6. Save FAISS index
os.makedirs("vector_index", exist_ok=True)

faiss.write_index(index, "vector_index/python.index")

# 7. Save chunks
with open("vector_index/chunks.pkl", "wb") as f:
    pickle.dump(chunks, f)

print("FAISS index and chunks saved successfully!")