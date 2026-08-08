# Python RAG Knowledge Assistant

A Retrieval-Augmented Generation (RAG) based chatbot that answers Python-related questions using information retrieved from a custom Python knowledge base.

## 🚀 Features

- 📚 Uses Python documentation/PDFs as the knowledge base
- 🔎 Uses FAISS for semantic similarity search
- 🧠 Uses `all-MiniLM-L6-v2` for text embeddings
- 🤖 Uses Llama 3.2 through Ollama for answer generation
- ⚡ FastAPI backend
- 💻 React frontend
- 🎯 Answers are restricted to the retrieved knowledge context

## 🏗️ Architecture

User Question
      ↓
React Frontend
      ↓
FastAPI Backend
      ↓
Question Embedding
      ↓
FAISS Vector Search
      ↓
Relevant Knowledge Chunks
      ↓
Llama 3.2
      ↓
Generated Answer
      ↓
React Frontend

## 🛠️ Technologies Used

- Python
- FastAPI
- React.js
- FAISS
- Sentence Transformers
- Llama 3.2
- Ollama
- Vite

## 📁 Project Structure

```text
projectRAG/
│
├── app.py
├── rag.py
├── ingest.py
├── requirements.txt
├── .env
├── .gitignore
│
├── PDFs/
│   └── Python documentation PDFs
│
├── vector_index/
│   ├── python.index
│   └── chunks.pkl
│
└── frontend/
    └── React application



⚙️ How It Works
1.Python documentation is provided as the knowledge source.
2.ingest.py processes the documents and divides them into text chunks.
3.The chunks are converted into embeddings using all-MiniLM-L6-v2.
4.FAISS stores these embeddings for fast similarity search.
5.When a user asks a question, the question is converted into an embedding.
6.FAISS retrieves the most relevant chunks.
7.The retrieved context is passed to Llama 3.2.
8.Llama generates an answer based on the retrieved context.
9.FastAPI sends the answer back to the React frontend.


▶️ Running the Project
1. Clone the repository
git clone https://github.com/abhishekshebbar15/python-rag-chatbot.git
cd python-rag-chatbot

2. Install Python dependencies
pip install -r requirements.txt

3. Install Ollama
Install Ollama and make sure the Llama 3.2 model is available:
ollama pull llama3.2

4. Start Ollama
ollama serve

5. Generate the Vector Index
Before starting the backend, generate the FAISS vector index:
```bash
python ingest.py

6. Start the FastAPI backend
python -m uvicorn app:app --reload

The backend will run at:
http://127.0.0.1:8000

7. Start the frontend

Open another terminal:

cd frontend
npm install
npm run dev

The React application will then be available through the Vite development server.


🔐 Environment Variables

Create a .env file if required by the project.
Do not commit API keys or other secrets to GitHub.

🎯 Example

Question:

What is inheritance in Python?

The system retrieves relevant information from the Python knowledge base and provides an answer using Llama.

📌 Important

This project uses RAG rather than training a new language model.

The Llama model is used as the generation model, while the project's custom knowledge base provides the information used to answer questions.

👨‍💻 Author

Abhishek Hebbar