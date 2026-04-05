import streamlit as st
from PIL import Image, ImageDraw
from gtts import gTTS
import os

# -----------------------------
# CREATE ROBOT FACE (BETTER)
# -----------------------------
def create_robot_face():
    img = Image.new("RGB", (400, 400), "white")
    draw = ImageDraw.Draw(img)

    # Head
    draw.ellipse((50, 80, 350, 350), outline="black", width=5)

    # Inner face
    draw.ellipse((90, 120, 310, 320), outline="black", width=4)

    # Eyes
    draw.ellipse((140, 170, 180, 210), fill="black")
    draw.ellipse((220, 170, 260, 210), fill="black")

    # Smile
    draw.arc((150, 230, 250, 310), start=0, end=180, fill="black", width=4)

    # Antenna
    draw.line((200, 80, 200, 40), fill="black", width=4)
    draw.ellipse((185, 20, 215, 50), outline="black", width=3)

    # Side panels
    draw.rectangle((40, 180, 70, 260), outline="black", width=3)
    draw.rectangle((330, 180, 360, 260), outline="black", width=3)

    return img

# -----------------------------
# TEXT TO SPEECH (WORKS ONLINE)
# -----------------------------
def generate_voice():
    text = ("Hello World, this is Gesner Deslandes. "
            "I build software now. "
            "My company GlobalInternet.py is heading to humanoid projects, "
            "please stay tuned!")

    tts = gTTS(text=text, lang='en', tld='com')  # US voice
    tts.save("voice.mp3")

# -----------------------------
# STREAMLIT UI
# -----------------------------
st.title("🤖 Gesner Humanoid AI")

robot = create_robot_face()
st.image(robot, caption="Humanoid Robot")

if st.button("🔊 Speak"):
    generate_voice()
    
    audio_file = open("voice.mp3", "rb")
    st.audio(audio_file.read(), format="audio/mp3")
