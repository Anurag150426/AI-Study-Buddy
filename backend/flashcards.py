from rag import llm  # reuse your LLM
from pydantic import BaseModel
from typing import List
import json
import re  

def extract_json(s: str):
    try:
        match = re.search(r"\[.*\]", s, re.DOTALL)
        if match:
            return json.loads(match.group())
    except:
        pass
    return None

# Pydantic models
class Flashcard(BaseModel):
    question: str
    answer: str

class FlashcardResponse(BaseModel):
    flashcards: List[Flashcard]


# ✅ MAIN FUNCTION
def generate_flashcards(vectordb, num_flashcards=5):

    # get documents from vector DB
    docs = vectordb._collection.get()["documents"]

    # take limited clean text (important for good output)
    text = " ".join(docs[:3])[:2000]

    # ✅ STRONG PROMPT (forces JSON)
    prompt = f"""
You are an AI that ONLY returns valid JSON.

Create {num_flashcards} flashcards from the text.

STRICT RULES:
- Output ONLY JSON
- No explanation
- No markdown
- No extra text
-No text outside json
- Format EXACTLY:

[
  {{"question": "text", "answer": "text"}}
]

TEXT:
{text}
"""

    # call LLM
    response = llm.invoke(prompt).content.strip()

    # CLEAN RESPONSE
    if "```" in response:
        response = response.replace("```json", "").replace("```", "")

    # extract only JSON part
    start = response.find("[")
    end = response.rfind("]") + 1
    response = response[start:end]

    #  PARSE + VALIDATE
    try:
        data = json.loads(response)

        validated = FlashcardResponse(
            flashcards=[Flashcard(**item) for item in data]
        )

        return validated.flashcards

    except Exception as e:
        # fallback if LLM fails
        return [
            Flashcard(
                question="Error parsing flashcards",
                answer=str(e)
            )
        ]