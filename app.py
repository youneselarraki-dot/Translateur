import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

import streamlit as st
import pygame
from gtts import gTTS
from deep_translator import GoogleTranslator
from langdetect import detect, LangDetectException
import tempfile, time

# ===============================
# LANGUAGE MAPPING
# ===============================
language_mapping = {
    "English": "en",
    "French": "fr",
    "Arabic": "ar",
    "Spanish": "es",
    "German": "de",
    "Italian": "it",
    "Portuguese": "pt",
    "Russian": "ru",
    "Chinese (Simplified)": "zh-CN",
    "Japanese": "ja",
    "Korean": "ko"
}

def get_language_code(language_name):
    return language_mapping.get(language_name, "en")

# ===============================
# TRANSLATION FUNCTION
# ===============================
def translator_function(text, from_language, to_language):
    if from_language == "auto":
        try:
            from_language = detect(text)
        except LangDetectException:
            from_language = "en"
    return GoogleTranslator(source=from_language, target=to_language).translate(text)

# ===============================
# TEXT TO VOICE FUNCTION
# ===============================
def text_to_voice(text_data, to_language):
    if to_language == "auto":
        to_language = "en"

    pygame.mixer.init()
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
        temp_path = fp.name

    tts = gTTS(text=text_data, lang=to_language, slow=False)
    tts.save(temp_path)
    time.sleep(0.2)
    sound = pygame.mixer.Sound(temp_path)
    sound.play()
    while pygame.mixer.get_busy():
        time.sleep(0.1)
    pygame.mixer.quit()
    os.remove(temp_path)

# ===============================
# MAIN APP
# ===============================
def main():
    st.set_page_config(page_title="Text Processing App", page_icon="📚")

    page = st.sidebar.radio("Explore", [
        "Home",
        "OCR",
        "Text Translation",
        "Text Summary",
        "Voice Translator",
        "Chatbot 🤖"
    ])

    if page == "Home":
        st.title("Welcome to Text Processing App")
        st.write("Perform OCR, translation, summarize text, or translate voice.")
        st.image("https://murf.ai/resources/media/posts/111/34370533_2203.q702.012.F.m005.c7.language-course-2.jpg", width=680)
        st.write("Developed by Team : Berkhli-El Akari-El Arraki | 2026")

    elif page == "OCR":
        import ocr_module
        ocr_module.page()

    elif page == "Text Translation":
        import translate_text
        translate_text.page_2()

    elif page == "Text Summary":
        import summary_module
        summary_module.page()

    elif page == "Voice Translator":
        import translate_voice
        translate_voice.page_3()
    elif page == "Chatbot 🤖":
        import chatbot_module
        chatbot_module.page()

if __name__ == "__main__":
    main()
