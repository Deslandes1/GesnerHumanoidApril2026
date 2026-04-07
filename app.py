import streamlit as st
from PIL import Image, ImageDraw
import asyncio
import edge_tts
import time

# -----------------------------
# PAGE CONFIG (VERY IMPORTANT)
# -----------------------------
st.set_page_config(layout="centered")

# -----------------------------
# VOICE SETTINGS
# -----------------------------
voices = {
    "English": "en-US-GuyNeural",
    "French": "fr-FR-HenriNeural",
    "Spanish": "es-ES-AlvaroNeural"
}

# -----------------------------
# SPEECH (SHORTENED FOR VIDEO)
# -----------------------------
texts = {
    "English": "Official Online Voting System for Haiti. Built by Gesner Deslandes. Secure, multilingual, real-time election platform. Made in Haiti for the world.",
    "French": "Système de vote en ligne pour Haïti. Sécurisé, multilingue, avec résultats en temps réel. Créé par Gesner Deslandes.",
    "Spanish": "Sistema de votación en línea para Haití. Seguro, multilingüe y en tiempo real. Creado por Gesner Deslandes."
}

# -----------------------------
# CREATE ROBOT FACE
# -----------------------------
def create_face(mouth_open=False):
    img = Image.new("RGB", (300, 300), "white")
    draw = ImageDraw.Draw(img)

    draw.ellipse((30, 40, 270, 270), outline="black", width=4)

    draw.ellipse((90, 120, 120, 150), fill="black")
    draw.ellipse((180, 120, 210, 150), fill="black")

    if mouth_open:
        draw.ellipse((120, 180, 180, 230), outline="black", width=3)
    else:
        draw.line((120, 210, 180, 210), fill="black", width=3)

    return img

# -----------------------------
# GENERATE VOICE
# -----------------------------
async def generate_voice(text, voice):
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save("voice.mp3")

# -----------------------------
# DURATION
# -----------------------------
def estimate_duration(text):
    return len(text.split()) / 2.5

# -----------------------------
# COMPACT UI (NO SCROLL)
# -----------------------------
st.markdown("<h2 style='text-align:center;'>🤖 Gesner Humanoid AI</h2>", unsafe_allow_html=True)

# Flag
st.markdown(
    "<div style='text-align:center;'><img src='https://upload.wikimedia.org/wikipedia/commons/5/56/Flag_of_Haiti.svg' width='100'></div>",
    unsafe_allow_html=True
)

# Language + Button INLINE
col1, col2 = st.columns([1,1])

with col1:
    language = st.selectbox("Language", list(voices.keys()))

with col2:
    speak = st.button("▶️ Speak")

# Robot centered
frame = st.empty()
frame.image(create_face(False), use_container_width=False)

# -----------------------------
# ACTION
# -----------------------------
if speak:
    asyncio.run(generate_voice(texts[language], voices[language]))

    audio_file = open("voice.mp3", "rb")
    st.audio(audio_file.read(), format="audio/mp3")

    duration = estimate_duration(texts[language])

    start = time.time()
    while time.time() - start < duration:
        frame.image(create_face(True))
        time.sleep(0.2)
        frame.image(create_face(False))
        time.sleep(0.2)

    frame.image(create_face(False))
