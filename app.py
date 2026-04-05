import streamlit as st
from PIL import Image, ImageDraw
import asyncio
import edge_tts
import time
import os

# -----------------------------
# VOICE SETTINGS
# -----------------------------
voices = {
    "English": "en-US-GuyNeural",   # Male
    "French": "fr-FR-HenriNeural",  # Male
    "Spanish": "es-ES-AlvaroNeural" # Male
}

# -----------------------------
# TEXT PER LANGUAGE
# -----------------------------
texts = {
    "English": "Hello World, this is Gesner Deslandes. I build software now. My company GlobalInternet.py is heading to humanoid projects, please stay tuned!",
    "French": "Bonjour le monde, ici Gesner Deslandes. Je développe des logiciels maintenant. Mon entreprise GlobalInternet.py se dirige vers des projets humanoïdes, restez connectés!",
    "Spanish": "Hola mundo, soy Gesner Deslandes. Ahora desarrollo software. Mi empresa GlobalInternet.py se dirige hacia proyectos humanoides, manténganse atentos!"
}

# -----------------------------
# CREATE ROBOT FACE (WITH MOUTH STATES)
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

    # Mouth animation
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
# GENERATE VOICE FILE
# -----------------------------
async def generate_voice(text, voice):
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save("voice.mp3")

# -----------------------------
# STREAMLIT UI
# -----------------------------
st.title("🤖 Gesner Humanoid AI")

# Language selector
language = st.selectbox("🌍 Select Language", list(voices.keys()))

# Display face
frame = st.empty()
frame.image(create_face(False))

if st.button("▶️ Speak"):
    
    # Generate voice
    asyncio.run(generate_voice(texts[language], voices[language]))

    # Play audio
    audio_file = open("voice.mp3", "rb")
    st.audio(audio_file.read(), format="audio/mp3")

    # Animate mouth while speaking
    for i in range(20):
        frame.image(create_face(mouth_open=(i % 2 == 0)))
        time.sleep(0.2)
