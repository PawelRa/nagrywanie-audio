from io import BytesIO
import streamlit as st
from audiorecorder import audiorecorder

#
#Główna część programu
#
st.set_page_config(page_title="Notatki audio", layout="centered")

st.title("Notatki audio")
note_audio = audiorecorder(
    start_prompt="Nagraj notatkę",
    stop_prompt="Zatrzymaj nagrywanie",
)

if note_audio:
    audio = BytesIO()
    note_audio.export(audio, format="mp3")
    note_audio_bytes = audio.getvalue()
    st.audio(note_audio_bytes, format="audio/mp3")

