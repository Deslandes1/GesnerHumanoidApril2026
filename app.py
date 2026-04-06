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
# VOICE GENERATION (EDGE TTS)
# -----------------------------
async def generate_voice(text, voice):
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save("speech.mp3")


# -----------------------------
# ESTIMATE DURATION
# -----------------------------
def estimate_duration(text):
    words = len(text.split())
    return words / 2.5


# -----------------------------
# SPEECH CONTENT (NEW)
# -----------------------------
speech_text = """
Building Real Solutions with Python, Streamlit, and AI.

Hello everyone. My name is Gesner Deslandes, and I am the founder of GlobalInternet.py – an online software company based in Haiti, operating entirely from the cloud.

In just a few weeks, we have built a portfolio of production-ready applications that solve real problems for real people. Let me walk you through what we have created.

1. Play Chess Against the Machine – A Teaching Tool
We built an interactive chess app that teaches you how to win. It has four difficulty levels – from Easy to Super Smart – and explains every move in four languages. It shows your moves, AI moves, and game results, and even generates reports.

2. Haiti Archives Nationales Database
We created a secure national record system for storing citizen data, documents, and identity records with high-level privacy and minister-level control.

3. SCORPION – AI App Builder
SCORPION generates full applications from simple prompts like calculators, websites, or tools. It also analyzes media and writes reports.

4. Smart Radio & Media Suite
A browser tool that converts video and audio links into downloadable MP3 and MP4 files, and allows recording and analysis.

How we build so fast:
We use Python, Streamlit, GitHub, and AI tools to accelerate development while maintaining full control as architects.

GlobalInternet.py is a cloud-based company operating from Haiti, delivering software worldwide.

Thank you for listening. Let’s build something great together.
"""


# -----------------------------
# STREAMLIT UI
# -----------------------------
st.title("🤖 Gesner Humanoid AI")

frame = st.empty()
frame.image(create_face(False))

# -----------------------------
# SPEAK BUTTON
# -----------------------------
if st.button("▶️ Speak"):

    # FIXED VOICE (clean single male English voice for stability)
    voice = "en-US-GuyNeural"

    # Generate audio
    asyncio.run(generate_voice(speech_text, voice))

    # Play audio
    audio_file = open("speech.mp3", "rb")
    st.audio(audio_file.read(), format="audio/mp3")

    # Animate mouth
    duration = estimate_duration(speech_text)

    start = time.time()
    while time.time() - start < duration:
        frame.image(create_face(True))
        time.sleep(0.2)
        frame.image(create_face(False))
        time.sleep(0.2)

    frame.image(create_face(False))
