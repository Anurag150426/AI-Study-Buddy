from fastapi import FastAPI, UploadFile, File
from dotenv import load_dotenv
import os
import shutil
import tempfile
from rag import create_vector_store, ask_question
from summarize import summarize
from file_handler import process_file

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

app = FastAPI()
vector_store = None  # initialize here

@app.get("/")
def home():
    return {"message": "AI Study Buddy API running!"}
@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    global vector_store
    
    # save temp file
    file_path = os.path.join(
        tempfile.gettempdir(), file.filename
    )
    with open(file_path, "wb") as f:
        shutil.copyfileobj(file.file, f)
    
    # detect and process any file type
    vector_store = create_vector_store(file_path)
    
    if vector_store is None:
        return {
            "error": "Unsupported file type!",
            "supported": ["pdf", "docx", "txt",
                         "pptx", "json", "jpg", "png"]
        }
    
    os.remove(file_path)
    
    return {
        "message": f"{file.filename} processed! ✅",
        "file_type": file.filename.split('.')[-1],
        "pages": len(vector_store.get())
    }

@app.post("/ask")
def ask_question_endpoint(question: str):
    if vector_store is None:
        return {"error": "Upload a PDF first!"}
    
    answer = ask_question(vector_store, question)
    return {"answer": answer}
@app.get("/summarize")
def summarize_endpoint():
    if vector_store is None:
        return {"error": "Upload a PDF first!"}
    
    summary = summarize(vector_store)
    return {"summary": summary}

@app.get("/flashcards")
def flashcards_endpoint():
    if vector_store is None:
        return {"error": "Upload a file first!"}
    
    from flashcards import generate_flashcards
    flashcards = generate_flashcards(vector_store, 5)

    return {
        "flashcards": [card.model_dump() for card in flashcards]
    }