import streamlit as st
from PIL import Image, ImageDraw
import asyncio
import edge_tts
import time
from pydub import AudioSegment

# -----------------------------
# BROWN HUMANOID FACE
# -----------------------------
def create_face(mouth_open=False):
    img = Image.new("RGB", (400, 400), "white")
    draw = ImageDraw.Draw(img)

    skin = (139, 69, 19)  # brown color

    # Head
    draw.ellipse((50, 80, 350, 350), fill=skin, outline="black", width=5)

    # Eyes
    draw.ellipse((140, 170, 180, 210), fill="white")
    draw.ellipse((150, 180, 170, 200), fill="black")

    draw.ellipse((220, 170, 260, 210), fill="white")
    draw.ellipse((230, 180, 250, 200), fill="black")

    # Mouth animation
    if mouth_open:
        draw.ellipse((170, 240, 230, 300), fill="black")
    else:
        draw.arc((150, 230, 250, 300), start=0, end=180, fill="black", width=4)

    # Antenna
    draw.line((200, 80, 200, 40), fill="black", width=4)
    draw.ellipse((185, 20, 215, 50), fill="black")

    return img

# -----------------------------
# GENERATE VOICE
# -----------------------------
async def generate_voice(text, voice):
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save("speech.mp3")

# -----------------------------
# GET AUDIO DURATION
# -----------------------------
def get_audio_duration(file):
    audio = AudioSegment.from_file(file)
    return len(audio) / 1000  # seconds

# -----------------------------
# STREAMLIT UI
# -----------------------------
st.title("🤖 Gesner Humanoid AI")

# Language selection
language = st.selectbox("🌍 Select Language", ["English", "French", "Spanish"])

voices = {
    "English": "en-US-GuyNeural",
    "French": "fr-FR-HenriNeural",
    "Spanish": "es-ES-AlvaroNeural"
}

# YOUR FULL SPEECH
speech_text = """Hello everyone. My name is Gesner Deslandes, and I am the founder of GlobalInternet.py – an online software company based in Haiti, operating entirely from the cloud.

In just a few weeks, we have built a portfolio of production-ready applications that solve real problems for real people.

We built an interactive chess app that teaches you how to win.

We created a secure digital record-keeping system for the Haitian government.

We built SCORPION, an AI assistant that creates applications.

We developed a smart radio and media suite.

All of this was built using Python, Streamlit, GitHub, and AI assistants.

GlobalInternet.py is a fully online company serving clients worldwide.

Thank you for listening. Let’s build something great together."""

# Face placeholder
frame = st.empty()
frame.image(create_face(False))

# BUTTON
if st.button("▶️ Speak"):

    # Generate voice
    asyncio.run(generate_voice(speech_text, voices[language]))

    # Play audio
    audio_file = open("speech.mp3", "rb")
    st.audio(audio_file.read(), format="audio/mp3")

    # Get duration
    duration = get_audio_duration("speech.mp3")

    # Animate EXACTLY for speech duration
    start_time = time.time()

    while time.time() - start_time < duration:
        frame.image(create_face(mouth_open=True))
        time.sleep(0.2)
        frame.image(create_face(mouth_open=False))
        time.sleep(0.2)

    # Ensure mouth closes at end
    frame.image(create_face(False))
