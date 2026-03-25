from rag import llm   # 🔥 reuse same LLM (important)

def summarize(vectordb):
    # 🔹 Step 1: get all documents
    docs = vectordb._collection.get()["documents"][:20]

    # 🔹 Step 2: MAP
    chunk_summaries = []

    for doc in docs:
        prompt = f"""
        You are a strict summarizer.

        Rules:
        - Only use the given text
        - Do NOT add extra information
        - Keep important details
        - Answer the question in simple plain text.
        - No special characters.
        - No newline characters.
        - Use spaces between sentences.


        Text:
        {doc}

        Summary:
        """

        response = llm.invoke(prompt)
        chunk_summaries.append(response.content)

    # 🔹 Step 3: REDUCE
    combined = " ".join(chunk_summaries)

    # prevent token overflow
    combined = combined[:12000]

    final_prompt = f"""
    Create a final structured summary.

    Rules:
    - No hallucination
    - Cover all key ideas
    - Be concise but complete
    - Answer the question in simple plain text.
    - Strictly no newline characters.
    - Use spaces between sentences.


    Format:
    - Key Topics
    - Important Points
    - Conclusion

    Text:
    {combined}

    Final Summary:
    """

    final_response = llm.invoke(final_prompt).content
    cleaned_response = final_response.replace("\n", " ").strip()

    return cleaned_response