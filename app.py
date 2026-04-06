import streamlit as st
from PIL import Image, ImageDraw
import time
import edge_tts

# -----------------------------
# HUMANOID FACE
# -----------------------------
def create_face(mouth_open=False):
    img = Image.new("RGB", (400, 400), "white")
    draw = ImageDraw.Draw(img)

    skin = (139, 69, 19)

    # Head
    draw.ellipse((50, 80, 350, 350), fill=skin, outline="black", width=5)

    # Eyes
    draw.ellipse((140, 170, 180, 210), fill="white")
    draw.ellipse((150, 180, 170, 200), fill="black")

    draw.ellipse((220, 170, 260, 210), fill="white")
    draw.ellipse((230, 180, 250, 200), fill="black")

    # Mouth
    if mouth_open:
        draw.ellipse((170, 240, 230, 300), fill="black")
    else:
        draw.arc((150, 230, 250, 300), start=0, end=180, fill="black", width=4)

    # Antenna
    draw.line((200, 80, 200, 40), fill="black", width=4)
    draw.ellipse((185, 20, 215, 50), fill="black")

    return img


# -----------------------------
# NATURAL SPEECH GENERATION (FIXED)
# -----------------------------
def generate_voice(text, voice, lang):
    communicate = edge_tts.Communicate(
        text,
        voice,
        rate="+0%",
        pitch="+0Hz"
    )
    communicate.save_sync("speech.mp3")


def estimate_duration(text):
    return len(text.split()) / 2.3


# -----------------------------
# UI
# -----------------------------
st.title("🤖 Gesner Humanoid AI")

language = st.selectbox("🌍 Select Language", ["English", "French"])

# -----------------------------
# BEST AVAILABLE NATURAL MALE VOICES
# -----------------------------
voices = {
    # 🇺🇸 Natural US male voice
    "English": "en-US-GuyNeural",

    # 🇫🇷 BEST natural French male voice (IMPORTANT FIX)
    "French": "fr-FR-HenriNeural"
}

speech_text = {
    "English": """
Hello everyone. My name is Gesner Deslandes, and I am the founder of GlobalInternet.py.
We build real software solutions using Python, Streamlit, GitHub, and AI.
Thank you for listening.
""",

    "French": """
Bonjour à tous. Je m'appelle Gesner Deslandes, et je suis le fondateur de GlobalInternet.py.
Nous créons des solutions logicielles réelles avec Python, Streamlit, GitHub et l'intelligence artificielle.
Merci de votre écoute.
"""
}

# -----------------------------
# DISPLAY FACE
# -----------------------------
frame = st.empty()
frame.image(create_face(False))

# -----------------------------
# SPEAK BUTTON
# -----------------------------
if st.button("▶️ Speak"):

    generate_voice(
        speech_text[language],
        voices[language],
        language
    )

    with open("speech.mp3", "rb") as audio_file:
        st.audio(audio_file.read(), format="audio/mp3")

    duration = estimate_duration(speech_text[language])

    start = time.time()
    while time.time() - start < duration:
        frame.image(create_face(True))
        time.sleep(0.2)
        frame.image(create_face(False))
        time.sleep(0.2)

    frame.image(create_face(False))
