import streamlit as st
from PIL import Image, ImageDraw
import time
from gtts import gTTS
import base64
import os

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(page_title="Gesner Humanoid AI", layout="wide")

# =========================
# TEXT TO SPEECH FUNCTION
# =========================
def text_to_audio(text, lang="fr"):
    tts = gTTS(text=text, lang=lang)
    audio_file = "speech.mp3"
    tts.save(audio_file)
    return audio_file


def autoplay_audio(file_path):
    with open(file_path, "rb") as f:
        data = f.read()
        b64 = base64.b64encode(data).decode()

    audio_html = f"""
    <audio autoplay controls>
        <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
    </audio>
    """
    st.markdown(audio_html, unsafe_allow_html=True)


# =========================
# SAFE TALKING FACE
# =========================
def create_face(mouth_level=0):
    img = Image.new("RGB", (400, 400), "white")
    draw = ImageDraw.Draw(img)

    # head
    draw.ellipse((50, 80, 350, 350), outline="black", width=5)

    # face inner
    draw.ellipse((90, 120, 310, 320), outline="black", width=3)

    # eyes
    draw.ellipse((140, 170, 180, 210), fill="black")
    draw.ellipse((220, 170, 260, 210), fill="black")

    # =========================
    # FIXED TALKING MOUTH
    # =========================
    mouth_width = 70
    base_y = 250

    open_amount = int(5 + mouth_level * 30)

    x1 = 200 - mouth_width // 2
    y1 = base_y
    x2 = 200 + mouth_width // 2
    y2 = base_y + open_amount

    draw.ellipse([x1, y1, x2, y2], outline="black", width=4)

    # antenna
    draw.line((200, 80, 200, 40), fill="black", width=4)
    draw.ellipse((185, 20, 215, 50), outline="black", width=3)

    return img


# =========================
# UI HEADER
# =========================
st.title("🤖 Gesner Humanoid AI Face")

text = st.text_area("Enter speech text:", "Hello, I am Gesner Humanoid AI speaking now.")

lang = st.selectbox("Language", ["fr", "en"])

# =========================
# SPEAK BUTTON
# =========================
if st.button("🔊 Speak"):

    # create audio
    audio_file = text_to_audio(text, lang)

    # estimate duration (safe approximation)
    duration = max(3, len(text) * 0.06)

    # play audio
    autoplay_audio(audio_file)

    # animation container
    frame = st.empty()

    start_time = time.time()

    # animate mouth until audio ends
    while time.time() - start_time < duration:

        # oscillation for talking effect
        for level in [0.2, 0.5, 1.0, 0.4, 0.7, 0.1]:
            img = create_face(level)
            frame.image(img)
            time.sleep(0.08)

    # final closed mouth
    frame.image(create_face(0))
