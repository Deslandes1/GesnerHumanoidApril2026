import streamlit as st
from gtts import gTTS
import uuid
import time
import os

st.set_page_config(page_title="Gesner Humanoid AI 🇭🇹", layout="centered")

# 🇭🇹 EXACT SCRIPT (HIDDEN — NEVER DISPLAYED)
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

# 🎤 Voice engine
def speak(text):
    filename = f"voice_{uuid.uuid4().hex}.mp3"
    tts = gTTS(text=text, lang="en")
    tts.save(filename)
    return filename

# 🤖 Humanoid Face (REAL UI STYLE)
def humanoid_face(mouth_open=False):
    mouth = "🔴" if mouth_open else "⚪"

    st.markdown(f"""
    <div style="
        text-align:center;
        padding:20px;
        background:linear-gradient(180deg,#0f172a,#1e293b);
        border-radius:20px;
        color:white;
    ">
        <div style="font-size:70px;">🇭🇹</div>
        <div style="font-size:110px;">🤖</div>
        <div style="font-size:40px; margin-top:-10px;">{mouth}</div>
        <div style="font-size:18px; margin-top:10px; opacity:0.7;">
            GESNER HUMANOID AI SYSTEM
        </div>
    </div>
    """, unsafe_allow_html=True)

# UI
st.title("🇭🇹 Gesner Humanoid AI")

humanoid_face(False)

if st.button("▶️ Activate Humanoid AI"):
    humanoid_face(True)

    with st.spinner("AI is speaking..."):
        audio_file = speak(SCRIPT)

    audio_bytes = open(audio_file, "rb").read()
    st.audio(audio_bytes, autoplay=True)

    # 🟡 lip sync animation loop
    for _ in range(8):
        humanoid_face(True)
        time.sleep(0.25)
        humanoid_face(False)
        time.sleep(0.25)

    os.remove(audio_file)

st.markdown("<center style='color:gray;'>Powered by GlobalInternet.py</center>", unsafe_allow_html=True)
