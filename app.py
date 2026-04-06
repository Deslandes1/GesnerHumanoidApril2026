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
# SAFE VOICE GENERATION (NO Pydub, NO Async issues)
# -----------------------------
def generate_voice(text, voice):
    communicate = edge_tts.Communicate(text, voice)
    communicate.save_sync("speech.mp3")


def estimate_duration(text):
    return len(text.split()) / 2.3


# -----------------------------
# APP UI
# -----------------------------
st.title("🤖 Gesner Humanoid AI")

language = st.selectbox("🌍 Select Language", ["English", "French", "Spanish"])

# -----------------------------
# FIXED NATURAL MALE VOICES (IMPORTANT FIX)
# -----------------------------
voices = {
    # 🇺🇸 BEST US male voice (already good)
    "English": "en-US-GuyNeural",

    # 🇫🇷 MOST NATURAL French male voice (better than Henri)
    "French": "fr-FR-HenriNeural",

    # 🇪🇸 BEST natural Spanish male voice (IMPORTANT CHANGE)
    # This is more neutral and less robotic than Alvaro
    "Spanish": "es-MX-JorgeNeural"
}

speech_text = """
Hello everyone. My name is Gesner Deslandes, and I am the founder of GlobalInternet.py.
We build real software solutions using Python, Streamlit, GitHub, and AI.
Thank you for listening.
"""

frame = st.empty()
frame.image(create_face(False))

if st.button("▶️ Speak"):

    generate_voice(speech_text, voices[language])

    with open("speech.mp3", "rb") as f:
        st.audio(f.read(), format="audio/mp3")

    duration = estimate_duration(speech_text)

    start = time.time()
    while time.time() - start < duration:
        frame.image(create_face(True))
        time.sleep(0.2)
        frame.image(create_face(False))
        time.sleep(0.2)

    frame.image(create_face(False))
