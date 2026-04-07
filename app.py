import streamlit as st
from PIL import Image, ImageDraw
import asyncio
import edge_tts
import time

# -----------------------------
# PAGE CONFIG
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
# SPEECH
# -----------------------------
texts = {
    "English": """Official Online Voting System for Haiti Elections. Developed by GlobalInternet.py. Built in Haiti for the world.""",
    "French": """Système de vote en ligne pour Haïti. Solution sécurisée et moderne développée en Haïti.""",
    "Spanish": """Sistema de votación en línea para Haití. Solución segura y moderna."""
}

# -----------------------------
# ORIGINAL HUMANOID FACE (RESTORED)
# -----------------------------
def create_face(mouth_open=False):
    img = Image.new("RGB", (400, 400), "white")
    draw = ImageDraw.Draw(img)

    # Head
    draw.ellipse((50, 80, 350, 350), outline="black", width=5)

    # Inner face
    draw.ellipse((90, 120, 310, 320), outline="black", width=4)

    # Eyes
    draw.ellipse((140, 170, 180, 210), fill="black")
    draw.ellipse((220, 170, 260, 210), fill="black")

    # Mouth
    if mouth_open:
        draw.ellipse((170, 240, 230, 300), outline="black", width=4)
    else:
        draw.arc((150, 230, 250, 300), start=0, end=180, fill="black", width=4)

    # Antenna
    draw.line((200, 80, 200, 40), fill="black", width=4)
    draw.ellipse((185, 20, 215, 50), outline="black", width=3)

    # Side panels
    draw.rectangle((40, 180, 70, 260), outline="black", width=3)
    draw.rectangle((330, 180, 360, 260), outline="black", width=3)

    return img

# -----------------------------
# VOICE GENERATION
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
# UI
# -----------------------------
st.title("🤖 Gesner Humanoid AI")

# 🇭🇹 FLAG (RESTORED CLEAN)
st.markdown(
    "<div style='text-align:center;'><img src='https://upload.wikimedia.org/wikipedia/commons/5/56/Flag_of_Haiti.svg' width='120'></div>",
    unsafe_allow_html=True
)

# Language
language = st.selectbox("🌍 Select Language", list(voices.keys()))

# Face
frame = st.empty()
frame.image(create_face(False))

# Button
if st.button("▶️ Speak"):

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
