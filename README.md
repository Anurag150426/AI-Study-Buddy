# 🧠 AI Study Buddy

AI-powered study assistant that helps
students learn smarter from their notes.

## Features
- Upload PDF, Word, Images, Text files
- Auto summarization
- Flashcard generation
- Chat with your notes (RAG)

## Tech Stack
- FastAPI + LangChain + ChromaDB
- Groq LLM (Llama 3.1)
- HuggingFace Embeddings
- Streamlit UI

## Setup
pip install -r requirements.txt
uvicorn backend/main:app --reload
streamlit run app.py