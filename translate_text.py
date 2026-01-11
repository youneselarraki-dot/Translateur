import streamlit as st
import app
from langdetect import detect, LangDetectException
import language_tool_python
import pygame

@st.cache_resource
def get_language_tool():
    return language_tool_python.LanguageTool('en-US')

def count_words(text):
    return len(text.split())

def page_2():
    st.title("🌍 Translate Text (Optional Correction)")

    # ===============================
    # OPTIONS
    # ===============================
    to_language = st.selectbox(
        "Select Target Language:",
        list(app.language_mapping.keys())
    )

    apply_correction = st.checkbox("✏️ Apply automatic correction before translation")

    # ===============================
    # INPUT
    # ===============================
    st.subheader("Enter text (any language):")
    sentence = st.text_area("Input Text", height=180)

    # ===============================
    # AUDIO BUTTONS
    # ===============================
    col1, col2, col3 = st.columns(3)
    play_input = col1.button("▶ Play Used Text")
    play_output = col2.button("▶ Play Translation")
    stop_audio = col3.button("⏹ Stop")

    detected_language_code = "en"
    corrected_text = ""
    text_to_translate = ""
    translation = ""

    if sentence.strip():
        # ===============================
        # LANGUAGE DETECTION
        # ===============================
        try:
            detected_language_code = detect(sentence)
        except LangDetectException:
            detected_language_code = "en"

        detected_language = next(
            (name for name, code in app.language_mapping.items() if code == detected_language_code),
            detected_language_code
        )
        st.info(f"Detected language: **{detected_language}**")

        # ===============================
        # CORRECTION (OPTIONAL)
        # ===============================
        if apply_correction:
            try:
                tool = get_language_tool()
                matches = tool.check(sentence)
                corrected_text = language_tool_python.utils.correct(sentence, matches)
                text_to_translate = corrected_text

                st.subheader("✏️ Corrected Text")
                st.write(corrected_text)

                st.write(f"📝 Words (Corrected): **{count_words(corrected_text)}**")

            except Exception:
                text_to_translate = sentence
                st.warning("Correction failed, using original text.")

        else:
            text_to_translate = sentence

        st.write(f"📝 Words (Used for translation): **{count_words(text_to_translate)}**")

        # ===============================
        # TRANSLATION
        # ===============================
        try:
            translation = app.translator_function(
                text_to_translate,
                detected_language_code,
                app.get_language_code(to_language)
            )

            st.subheader("✅ Translation")
            st.success(translation)
            st.write(f"📝 Words (Translation): **{count_words(translation)}**")

        except Exception as e:
            st.error(f"Translation error: {e}")

        # ===============================
        # DOWNLOAD
        # ===============================
        st.subheader("📥 Download")

        d1, d2, d3 = st.columns(3)

        d1.download_button(
            "⬇ Input Text",
            sentence,
            file_name="input_text.txt",
            mime="text/plain"
        )

        if apply_correction:
            d2.download_button(
                "⬇ Corrected Text",
                corrected_text,
                file_name="corrected_text.txt",
                mime="text/plain"
            )

        d3.download_button(
            "⬇ Translation",
            translation,
            file_name="translated_text.txt",
            mime="text/plain"
        )

    # ===============================
    # AUDIO
    # ===============================
    if play_input and text_to_translate:
        app.text_to_voice(text_to_translate, detected_language_code)

    if play_output and translation:
        app.text_to_voice(translation, app.get_language_code(to_language))

    if stop_audio:
        try:
            pygame.mixer.stop()
            st.info("Audio stopped.")
        except Exception:
            st.warning("No audio playing.")
