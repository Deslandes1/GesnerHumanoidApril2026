import streamlit as st
from gtts import gTTS
import uuid
import time
import os

st.set_page_config(page_title="Gesner Humanoid AI 🇭🇹", layout="centered")

# 🇭🇹 FULL SCRIPT (HIDDEN)
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

# 🎤 voice
def speak(text):
    filename = f"voice_{uuid.uuid4().hex}.mp3"
    tts = gTTS(text=text, lang="en")
    tts.save(filename)
    return filename

# 🤖 face UI (stable frame)
def face(open_mouth=False):
    mouth = "🔴" if open_mouth else "⚪"

    st.markdown(f"""
    <div style="
        text-align:center;
        background:#0f172a;
        padding:30px;
        border-radius:25px;
        color:white;
    ">
        <div style="font-size:60px;">🇭🇹</div>
        <div style="font-size:120px;">🤖</div>
        <div style="font-size:45px;">{mouth}</div>
        <div style="opacity:0.7;">GESNER HUMANOID AI</div>
    </div>
    """, unsafe_allow_html=True)

st.title("🇭🇹 Gesner Humanoid AI")

face(False)

if st.button("▶️ START AI"):
    audio_file = speak(SCRIPT)

    audio_bytes = open(audio_file, "rb").read()
    st.audio(audio_bytes, autoplay=True)

    # ⏱️ approximate speech duration (based on text length)
    estimated_duration = max(8, len(SCRIPT.split()) * 0.35)

    start = time.time()

    while time.time() - start < estimated_duration:
        face(True)
        time.sleep(0.25)
        face(False)
        time.sleep(0.25)

    os.remove(audio_file)

st.markdown("<center style='color:gray;'>GlobalInternet.py AI System 🇭🇹</center>", unsafe_allow_html=True)
