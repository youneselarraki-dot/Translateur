import streamlit as st
from transformers import pipeline

# Crée le pipeline de résumé (sera téléchargé automatiquement)
@st.cache_resource  # pour éviter de retélécharger à chaque fois
def get_summarizer():
    return pipeline("summarization")

def page():
    st.title("Text Summary")

    input_text = st.text_area("Enter text to summarize:", height=300)
    max_length = st.slider("Maximum length of summary", 30, 200, 100)
    min_length = st.slider("Minimum length of summary", 10, 50, 25)

    if st.button("Generate Summary"):
        if not input_text.strip():
            st.warning("Please enter some text first.")
            return
        try:
            summarizer = get_summarizer()
            summary = summarizer(
                input_text,
                max_length=max_length,
                min_length=min_length,
                do_sample=False
            )
            summary_text = summary[0]['summary_text']
            st.subheader("Summary")
            st.write(summary_text)
        except Exception as e:
            st.error(f"Error generating summary: {e}")
