import streamlit as st
import easyocr
import app
from langdetect import detect, LangDetectException
import pygame

def create_reader(languages):
    if "ch_sim" in languages:
        return easyocr.Reader(['ch_sim', 'en'], gpu=False)
    else:
        return easyocr.Reader(languages, gpu=False)

def page():
    st.title("🖼 OCR + Detection + Translation")

    # OCR languages
    ocr_languages = {
        "English": "en",
        "French": "fr",
        "Arabic": "ar",
        "Spanish": "es",
        "German": "de",
        "Italian": "it",
        "Portuguese": "pt",
        "Russian": "ru",
        "Chinese (Simplified)": "ch_sim",
        "Japanese": "ja",
        "Korean": "ko"
    }

    selected_languages = st.multiselect(
        "OCR languages (image text):",
        list(ocr_languages.keys()),
        default=["English"]
    )

    if not selected_languages:
        st.warning("Please select at least one OCR language.")
        return

    reader = create_reader([ocr_languages[l] for l in selected_languages])

    # Translation target
    target_lang_name = st.selectbox(
        "Translate to:",
        list(app.language_mapping.keys())
    )
    target_lang = app.get_language_code(target_lang_name)

    uploaded_file = st.file_uploader(
        "Upload an image",
        type=["png", "jpg", "jpeg"]
    )

    if uploaded_file is not None:
        st.image(
            uploaded_file,
            caption="Uploaded Image",
            use_container_width=True   # ✅ FIXED
        )

        with st.spinner("Extracting text..."):
            result = reader.readtext(uploaded_file.read())

        extracted_text = " ".join([text[1] for text in result])

        if not extracted_text.strip():
            st.warning("No text detected.")
            return

        st.subheader("📄 Extracted Text")
        st.write(extracted_text)

        # Detect language
        try:
            detected_code = detect(extracted_text)
        except LangDetectException:
            detected_code = "en"

        detected_name = next(
            (n for n, c in app.language_mapping.items() if c == detected_code),
            detected_code
        )
        st.info(f"Detected language: **{detected_name}**")

        # Translate
        translated_text = app.translator_function(
            extracted_text,
            detected_code,
            target_lang
        )

        st.subheader("🌍 Translated Text")
        st.success(translated_text)

        # AUDIO CONTROLS
        col1, col2 = st.columns(2)

        with col1:
            if st.button("▶ Play Audio"):
                app.text_to_voice(translated_text, target_lang)

        with col2:
            if st.button("⏹ Stop Audio"):
                try:
                    pygame.mixer.stop()
                    st.info("Audio stopped.")
                except:
                    st.warning("No audio playing.")
