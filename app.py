import streamlit as st
from gtts import gTTS
import uuid
import base64
import time
import os

st.set_page_config(page_title="Gesner Humanoid AI", layout="centered")

# 🧠 EXACT SCRIPT (NOT DISPLAYED)
SCRIPT = """
GlobalInternet.py – Build with Python. Deliver with Speed.

We don’t just write code. We build complete, production-ready software on demand – tailored to your needs, delivered by email in record time.

What we do:
Custom web applications Streamlit Flask Django
Election and voting systems
AI powered tools chatbots data analysis automation
Business dashboards reporting tools internal workflows
Any Python based project you can imagine we make it work online

Who we are:
GlobalInternet.py was founded by Gesner Deslandes owner founder and lead engineer.
Like Silicon Valley but with a Haitian touch and outstanding outcomes.
We leverage AI and modern Python frameworks to build fast reliable and scalable solutions.

Our promise:
We are an online company working for the world.
No matter where you are we deliver the full software package via email ready to install and use.

Contact us right now
Phone WhatsApp 509 47385663
Email deslandes78@gmail.com

GlobalInternet.py Your Python partner from Haiti to the world.
"""

# 🎤 TTS generator
def speak(text):
    filename = f"voice_{uuid.uuid4().hex}.mp3"
    tts = gTTS(text=text, lang="en")
    tts.save(filename)
    return filename

# 🧑 Humanoid face (simple animated mouth)
def humanoid_face(moving=False):
    mouth = "🟡" if moving else "⚪"
    face_html = f"""
    <div style="text-align:center;">
        <div style="font-size:120px;">🤖</div>
        <div style="font-size:50px; margin-top:-20px;">{mouth}</div>
    </div>
    """
    st.markdown(face_html, unsafe_allow_html=True)

st.title("🧠 Gesner Humanoid AI")

# Keep face always visible
humanoid_face(False)

if st.button("▶️ Start AI Speaking"):
    humanoid_face(True)

    with st.spinner("AI is speaking..."):
        audio_file = speak(SCRIPT)

    audio_bytes = open(audio_file, "rb").read()
    st.audio(audio_bytes, autoplay=True)

    # fake lip movement loop (simple animation effect)
    for _ in range(6):
        humanoid_face(True)
        time.sleep(0.3)
        humanoid_face(False)
        time.sleep(0.3)

    os.remove(audio_file)

# Keep UI clean (NO SCRIPT SHOWN)
st.markdown("<br><center>Gesner Humanoid AI System Online</center>", unsafe_allow_html=True)
