import streamlit as st
import whisper
from translate import Translator  # Using 'translate' package instead of googletrans
from gtts import gTTS
import os
from io import BytesIO
from pydub import AudioSegment

# Load Whisper model
@st.cache_resource
def load_model():
    return whisper.load_model("tiny")

model = load_model()

# SpeakVerse Branding
st.title("SpeakVerse 🎙️🌍")
st.subheader("Break the language barrier with multilingual audio translation!")

# Language mapping for gTTS
language_mapping = {
    "Urdu": "ur",
    "Arabic": "ar",
    "French": "fr",
    "Spanish": "es"
}

# Upload Audio File
st.header("Upload Audio File to SpeakVerse")
uploaded_file = st.file_uploader("Choose an audio file", type=["mp3", "wav"])

audio_path = None  # Initialize the audio path

if uploaded_file is not None:
    audio_path = "uploaded_audio.wav"
    audio_segment = AudioSegment.from_file(uploaded_file)
    audio_segment.export(audio_path, format="wav")
    st.audio(audio_path, format="audio/wav")

# Proceed if there's an audio file to process
if audio_path:
    # User selects the target language
    target_language = st.selectbox("Select Target Language:", ("Urdu", "Arabic", "French", "Spanish"))
    gtts_language = language_mapping[target_language]

    # Transcribe Audio using Whisper Model
    st.info("Transcribing audio with SpeakVerse...")
    result = model.transcribe(audio_path)
    text = result["text"]
    st.write("Transcribed Text:", text)

    if not text:
        st.error("No speech detected in the audio. Please try with a different file.")
    else:
        # Translate the text using translate package
        st.info("Translating text with SpeakVerse...")
        translator = Translator(to_lang=gtts_language)
        translated_text = translator.translate(text)
        st.write(f"Translated Text ({target_language}):", translated_text)

        if not translated_text:
            st.error("Translation failed. Please try again.")
        else:
            # Convert Translated Text to Speech using gTTS
            st.info("Converting translated text to speech with SpeakVerse...")
            tts = gTTS(translated_text, lang=gtts_language)
            translated_audio_path = "translated_audio.mp3"
            tts.save(translated_audio_path)
            st.audio(translated_audio_path, format="audio/mp3")

            # Provide download button for translated audio
            with open(translated_audio_path, "rb") as f:
                st.download_button("Download Translated Audio", data=f, file_name="translated_audio.mp3", mime="audio/mp3")

            # Cleanup temporary files
            os.remove(audio_path)
            os.remove(translated_audio_path)
