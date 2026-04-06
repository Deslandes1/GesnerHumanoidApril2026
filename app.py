import streamlit as st
from PIL import Image, ImageDraw
import asyncio
import edge_tts
import time

# -----------------------------
# HUMANOID FACE
# -----------------------------
def create_face(mouth_open=False):
    img = Image.new("RGB", (400, 400), "white")
    draw = ImageDraw.Draw(img)

    skin = (139, 69, 19)

    draw.ellipse((50, 80, 350, 350), fill=skin, outline="black", width=5)

    draw.ellipse((140, 170, 180, 210), fill="white")
    draw.ellipse((150, 180, 170, 200), fill="black")

    draw.ellipse((220, 170, 260, 210), fill="white")
    draw.ellipse((230, 180, 250, 200), fill="black")

    if mouth_open:
        draw.ellipse((170, 240, 230, 300), fill="black")
    else:
        draw.arc((150, 230, 250, 300), start=0, end=180, fill="black", width=4)

    draw.line((200, 80, 200, 40), fill="black", width=4)
    draw.ellipse((185, 20, 215, 50), fill="black")

    return img


# -----------------------------
# TTS FUNCTION
# -----------------------------
async def generate_voice(text, voice):
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save("speech.mp3")


def estimate_duration(text):
    return len(text.split()) / 2.5


# -----------------------------
# ENGLISH SPEECH
# -----------------------------
speech_english = """
Building Real Solutions with Python, Streamlit, and AI.

Hello everyone. My name is Gesner Deslandes, and I am the founder of GlobalInternet.py – an online software company based in Haiti, operating entirely from the cloud.

In just a few weeks, we have built a portfolio of production-ready applications that solve real problems for real people.

1. Play Chess Against the Machine – A Teaching Tool
We built an interactive chess app that teaches you how to win in four languages.

2. Haiti Archives Nationales Database
A secure digital record system for government data management.

3. SCORPION – AI App Builder
An AI system that builds full applications from simple prompts.

4. Smart Radio & Media Suite
A tool that converts media links into downloadable audio and video files.

All systems were built using Python, Streamlit, GitHub, and AI tools.

GlobalInternet.py is a cloud-based company operating from Haiti.

Thank you for listening.
"""


# -----------------------------
# FRENCH SPEECH (FULL NATURAL TRANSLATION)
# -----------------------------
speech_french = """
Construire de vraies solutions avec Python, Streamlit et l’intelligence artificielle.

Bonjour à tous. Je m’appelle Gesner Deslandes et je suis le fondateur de GlobalInternet.py – une entreprise de logiciels en ligne basée en Haïti et entièrement opérée depuis le cloud.

En seulement quelques semaines, nous avons créé un portefeuille d’applications prêtes à l’utilisation qui résolvent de vrais problèmes pour de vraies personnes.

1. Jouer aux échecs contre la machine – un outil d’apprentissage
Nous avons construit une application d’échecs interactive qui vous apprend à gagner en quatre langues.

2. Base de données des Archives Nationales d’Haïti
Un système sécurisé de gestion des données gouvernementales.

3. SCORPION – Constructeur d’applications IA
Un système d’intelligence artificielle capable de créer des applications complètes à partir de simples instructions.

4. Suite Radio et Médias Intelligents
Un outil qui convertit des liens multimédias en fichiers audio et vidéo téléchargeables.

Tous ces systèmes ont été développés avec Python, Streamlit, GitHub et des outils d’intelligence artificielle.

GlobalInternet.py est une entreprise basée dans le cloud opérant depuis Haïti.

Merci de votre attention.
"""


# -----------------------------
# VOICES
# -----------------------------
voices = {
    "English": "en-US-GuyNeural",
    "French": "fr-FR-HenriNeural"
}


# -----------------------------
# UI
# -----------------------------
st.title("🤖 Gesner Humanoid AI")

language = st.selectbox("🌍 Select Language", ["English", "French"])

frame = st.empty()
frame.image(create_face(False))


# -----------------------------
# SPEAK
# -----------------------------
if st.button("▶️ Speak"):

    text = speech_english if language == "English" else speech_french

    asyncio.run(generate_voice(text, voices[language]))

    audio_file = open("speech.mp3", "rb")
    st.audio(audio_file.read(), format="audio/mp3")

    duration = estimate_duration(text)

    start = time.time()
    while time.time() - start < duration:
        frame.image(create_face(True))
        time.sleep(0.2)
        frame.image(create_face(False))
        time.sleep(0.2)

    frame.image(create_face(False))
