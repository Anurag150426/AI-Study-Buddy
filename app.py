import streamlit as st
import requests

API="http://localhost:8000"

st.set_page_config(
    page_title="AI Study Buddy",
    page_icon="R",
    layout="wide"
)

st.title("AI STUDY BUDDY 🤖")
st.subheader("Upload your study materials and ask questions!")

with st.sidebar:
    st.header("Upload File")
    uploaded_file = st.file_uploader(
        "Choose a file (PDF, DOCX, TXT, PPTX, JSON, JPG, PNG)",
        type=["pdf", "docx", "txt", "pptx", "json", "jpg", "png"]
    )
    
    if uploaded_file is not None:
        with st.spinner("Uploading and processing..."):
            files = {"file": (uploaded_file.name, uploaded_file.getvalue())}
            response = requests.post(f"{API}/upload", files=files)
        
        if response.status_code == 200:
            st.success(response.json().get("message"))
        else:
            st.error(response.json().get("error"))

tab1, tab2, tab3 = st.tabs(["FlashCards", "Summarize","Chat"])
with tab1:
    if st.button("Generate Flashcards"):
        with st.spinner("Generating flashcards..."):
            response = requests.get(f"{API}/flashcards")

        if response.status_code == 200:
            flashcards = response.json().get("flashcards", [])

            # ✅ SAFETY CHECK
            if isinstance(flashcards, str):
                st.error("Flashcards not in correct format")
                st.write(flashcards)

            elif isinstance(flashcards, list):
                for idx, card in enumerate(flashcards):
                    if isinstance(card, dict):
                        st.markdown(f"**Q{idx+1}: {card.get('question', 'No question')}**")
                        st.markdown(f"- A: {card.get('answer', 'No answer')}")
                    else:
                        st.write(card)

        else:
            st.error(response.json().get("error"))

with tab2:
    if st.button("Summarize Content"):
        with st.spinner("Summarizing content..."):
            response = requests.get(f"{API}/summarize")
        
        if response.status_code == 200:
            summary = response.json().get("summary", "")
            st.markdown(f"**Summary:** {summary}")
        else:
            st.error(response.json().get("error"))

with tab3:
    question = st.text_input("Ask a question about your study materials:")
    if st.button("Get Answer"):
        with st.spinner("Getting answer..."):
            response = requests.post(f"{API}/ask", params={"question": question})
        
        if response.status_code == 200:
            answer = response.json().get("answer", "")
            st.markdown(f"**Answer:** {answer}")
        else:
            st.error(response.json().get("error"))                        
