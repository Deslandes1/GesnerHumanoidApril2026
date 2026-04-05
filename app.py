import streamlit as st
from PIL import Image, ImageDraw
import asyncio
import edge_tts
import time

# -----------------------------
# BROWN HUMANOID FACE
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
# VOICE GENERATION
# -----------------------------
async def generate_voice(text, voice):
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save("speech.mp3")

# -----------------------------
# ESTIMATE DURATION
# -----------------------------
def estimate_duration(text):
    words = len(text.split())
    return words / 2.5  # ~2.5 words per second

# -----------------------------
# STREAMLIT UI
# -----------------------------
st.title("🤖 Gesner Humanoid AI")

language = st.selectbox("🌍 Select Language", ["English", "French", "Spanish"])

voices = {
    "English": "en-US-GuyNeural",
    "French": "fr-FR-HenriNeural",
    "Spanish": "es-ES-AlvaroNeural"
}

speech_text = """Hello everyone. My name is Gesner Deslandes, and I am the founder of GlobalInternet.py. We build real software solutions using Python, Streamlit, GitHub, and AI. Thank you for listening. Let’s build something great together."""

frame = st.empty()
frame.image(create_face(False))

if st.button("▶️ Speak"):

    # Generate voice
    asyncio.run(generate_voice(speech_text, voices[language]))

    # Play audio
    audio_file = open("speech.mp3", "rb")
    st.audio(audio_file.read(), format="audio/mp3")

    # Estimate duration
    duration = estimate_duration(speech_text)

    # Animate
    start = time.time()
    while time.time() - start < duration:
        frame.image(create_face(True))
        time.sleep(0.2)
        frame.image(create_face(False))
        time.sleep(0.2)

    frame.image(create_face(False))
