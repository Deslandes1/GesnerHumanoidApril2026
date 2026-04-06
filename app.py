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
# VOICE GENERATION (STABLE)
# -----------------------------
def generate_voice(text, voice):
    communicate = edge_tts.Communicate(text, voice)
    communicate.save_sync("speech.mp3")


# -----------------------------
# ESTIMATE DURATION
# -----------------------------
def estimate_duration(text):
    words = len(text.split())
    return words / 2.5


# -----------------------------
# STREAMLIT UI
# -----------------------------
st.title("🤖 Gesner Humanoid AI")

language = st.selectbox(
    "🌍 Select Language",
    ["English", "French", "Spanish"]
)

# -----------------------------
# NATURAL MALE NATIVE VOICES
# -----------------------------
voices = {
    # 🇺🇸 English male (natural US voice)
    "English": "en-US-GuyNeural",

    # 🇫🇷 Native-sounding French male (Paris accent)
    "French": "fr-FR-HenriNeural",

    # 🇪🇸 Natural Spanish male (Latin-neutral, smoother global tone)
    "Spanish": "es-MX-JorgeNeural"
}

speech_text = """
Hello everyone. My name is Gesner Deslandes, and I am the founder of GlobalInternet.py.
We build real software solutions using Python, Streamlit, GitHub, and AI.
Thank you for listening. Let’s build something great together.
"""

# -----------------------------
# UI FRAME
# -----------------------------
frame = st.empty()
frame.image(create_face(False))

# -----------------------------
# BUTTON ACTION
# -----------------------------
if st.button("▶️ Speak"):

    # Generate speech
    generate_voice(speech_text, voices[language])

    # Play audio
    with open("speech.mp3", "rb") as audio_file:
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
