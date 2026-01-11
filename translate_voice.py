import streamlit as st
import speech_recognition as sr
import app
from langdetect import detect, LangDetectException
import pygame

def page_3():
    st.title("🎙 Translate your voice into multiple languages")

    # Init state
    if "listening" not in st.session_state:
        st.session_state.listening = False

    # Target language
    to_language_name = st.selectbox(
        "Select Target Language:",
        list(app.language_mapping.keys()),
        index=list(app.language_mapping.keys()).index("English")
    )
    to_language = app.get_language_code(to_language_name)

    # Buttons
    col1, col2 = st.columns(2)
    start_button = col1.button("▶ Start Listening")
    stop_button = col2.button("⏹ Stop")

    output_placeholder = st.empty()
    detected_placeholder = st.empty()
    translation_placeholder = st.empty()

    # START
    if start_button:
        st.session_state.listening = True

    # STOP
    if stop_button:
        st.session_state.listening = False
        try:
            pygame.mixer.stop()
        except:
            pass
        output_placeholder.info("Stopped.")
        return

    # LISTEN ONCE (SAFE)
    if st.session_state.listening:
        recognizer = sr.Recognizer()

        with sr.Microphone() as source:
            output_placeholder.text("🎤 Listening...")
            recognizer.pause_threshold = 1
            audio = recognizer.listen(source, phrase_time_limit=8)

        try:
            output_placeholder.text("⏳ Processing...")
            spoken_text = recognizer.recognize_google(audio)

            # Detect language
            try:
                detected_code = detect(spoken_text)
            except LangDetectException:
                detected_code = "en"

            detected_name = next(
                (name for name, code in app.language_mapping.items() if code == detected_code),
                detected_code
            )
            detected_placeholder.info(f"Detected language: **{detected_name}**")

            # Translate
            translated_text = app.translator_function(
                spoken_text,
                detected_code,
                to_language
            )
            translation_placeholder.success(translated_text)

            # Play TTS
            app.text_to_voice(translated_text, to_language)

        except Exception as e:
            output_placeholder.error(f"Error: {e}")

        # Relancer automatiquement
        st.rerun()
