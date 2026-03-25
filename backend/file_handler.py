from langchain_community.document_loaders import(
    PyPDFLoader,
    Docx2txtLoader,
    TextLoader,
    UnstructuredCSVLoader,
    UnstructuredEmailLoader,
    UnstructuredHTMLLoader,
    UnstructuredPowerPointLoader

)
from langchain_core.documents import Document
import easyocr
import os
import json

def process_file(file_path: str):
    ext=file_path.split(".")[-1].lower()
    if ext=="pdf":
        loader=PyPDFLoader(file_path)
        return loader.load()
    elif ext=="docx":
        loader=Docx2txtLoader(file_path)
        return loader.load()
    elif ext=="txt":
        loader=TextLoader(file_path)
        return loader.load()
    elif ext=="csv":
        loader=UnstructuredCSVLoader(file_path)
        return loader.load()

    elif ext in ["eml","email"]:
        loader=UnstructuredEmailLoader(file_path)
        return loader.load()

    elif ext in ["html","htm"]:
        loader=UnstructuredHTMLLoader(file_path)
        return loader.load()
    elif ext in ["ppt","pptx"]:
        loader=UnstructuredPowerPointLoader(file_path)
        return loader.load()
    else:
        raise ValueError("Unsupported file type")
    

def process_scanned_pdf(file_path: str):
    reader = easyocr.Reader(['en'])
    result = reader.readtext(file_path, detail=0)
    text = " ".join(result)
    return [Document(page_content=text, metadata={"source": file_path})]

def process_json(file_path: str):
    with open(file_path, "r") as f:
        data = json.load(f)
    text = json.dumps(data)
    return [Document(page_content=text, metadata={"source": file_path})]