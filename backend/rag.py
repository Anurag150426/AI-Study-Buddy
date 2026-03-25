from langchain_groq import ChatGroq
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
import os
from dotenv import load_dotenv

from file_handler import process_file

# load env
load_dotenv()

# LLM
llm = ChatGroq(
    model="llama-3.1-8b-instant",
    api_key=os.getenv("GROQ_API_KEY")
)

# Embeddings
embeddings = HuggingFaceEmbeddings(
    model_name="all-MiniLM-L6-v2"
)

# 🚀 NEW: universal vector store creator
def create_vector_store(file_path):
    # 1. load file (auto detects pdf/docx/etc)
    documents = process_file(file_path)

    # 2. split
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=150
    )
    texts = text_splitter.split_documents(documents)

    # 3. vector store
    vector_store = Chroma.from_documents(texts, embeddings)

    return vector_store


# ❓ Ask question (RAG)
def ask_question(vector_store, question: str):
    relevant_chunks = vector_store.similarity_search(question, k=3)

    context = " ".join(
        [chunk.page_content for chunk in relevant_chunks]
    )

    prompt = f"""
    Answer based only on the provided context.
    Explain clearly like a teacher.
    Give examples where needed.
    Do not hallucinate.
    Keep answer in plain text.
    No special formatting.

    Context: {context}
    Question: {question}
    Answer:
    """

    response = llm.invoke(prompt).content

    # clean output
    cleaned_response = response.replace("\n", " ").strip()

    return cleaned_response