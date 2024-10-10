import streamlit as st
from io import BytesIO
from audiorecorder import audiorecorder  # type: ignore
from dotenv import dotenv_values
from openai import OpenAI
from hashlib import md5

ENV = dotenv_values(".env")
AUDIO_TRANSCRIBE_MODEL = "whisper-1"

def get_openai_client():
    return OpenAI(api_key=st.session_state["openai_api_key"])
    # return OpenAI(api_key=ENV["OPENAI_API_KEY"])

def transcribe_audio(audio_bytes):
    openai_client = get_openai_client()
    audio_file = BytesIO(audio_bytes)
    audio_file.name = "audio.mp3"
    transcript = openai_client.audio.transcriptions.create(
        file=audio_file,
        model=AUDIO_TRANSCRIBE_MODEL,
        response_format="verbose_json",
    )    
    return transcript.text

#
# MAIN
#
st.set_page_config(page_title="Audio Notatki", layout="centered")

# OpenAI APU key
if not st.session_state.get("openai_api_key"):
    if "OPENAI_API_KEY" in ENV:
        st.session_state["openai_api_key"] = ENV["OPENAI_API_KEY"]

    else:
        st.info("Dodaj swój klucz API OpenAI, aby móc korzystać z tej aplikacji")
        st.session_state["openai_api_key"] = st.text_input("Klucz API", type="password")
        if st.session_state["openai_api_key"]:
            st.rerun()

if not st.session_state.get("openai_api_key"):
    st.stop()

# Sesion state initialization
if "note_audio_bytes_md5" not in st.session_state:
    st.session_state["note_audio_bytes_md5"] = None

if "note_audio_bytes" not in st.session_state:
    st.session_state["note_audio_bytes"] = None

if "note_audio_text" not in st.session_state:
    st.session_state["note_audio_text"] = ""

st.title("Audio Notatki")
note_audio = audiorecorder(
    start_prompt="Nagraj notatkę",
    stop_prompt="Zatrzymaj nagrywanie",
)

if note_audio:
    audio = BytesIO()
    note_audio.export(audio, format="mp3")
    st.session_state["note_audio_bytes"] = audio.getvalue()
    current_md5 = md5(st.session_state["note_audio_bytes"]).hexdigest()
    if st.session_state["note_audio_bytes_md5"] != current_md5:
        st.session_state["note_audio_text"] = ""
        st.session_state["note_audio_bytes_md5"] = current_md5        

    st.audio(st.session_state["note_audio_bytes"], format="audio/mp3")

    if st.button("Transkrybuj audio"):
        st.session_state["note_audio_text"] = transcribe_audio(st.session_state["note_audio_bytes"])

    if st.session_state["note_audio_text"]:
        st.text_area(
            "Transkrypcja audio",
            value=st.session_state["note_audio_text"],
            disabled=True,
        )
