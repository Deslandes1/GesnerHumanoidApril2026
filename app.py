import streamlit as st
from gtts import gTTS
import os
import uuid

st.set_page_config(page_title="GlobalInternet.py AI Voice", layout="centered")

# 🎤 EXACT SCRIPT (will NOT be displayed)
script = """
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
Phone or WhatsApp 509 47385663
Email deslandes78@gmail.com

Whether you need a company website a custom software tool or a full scale online platform we build it you own it.

GlobalInternet.py Your Python partner from Haiti to the world.
"""

def generate_audio(text):
    filename = f"speech_{uuid.uuid4().hex}.mp3"
    tts = gTTS(text=text, lang="en")
    tts.save(filename)
    return filename

st.title("🔊 GlobalInternet.py AI Voice System")

# Button only (no text display)
if st.button("▶️ Play AI Voice"):
    with st.spinner("Generating voice..."):
        audio_file = generate_audio(script)

    st.success("Ready")

    audio_bytes = open(audio_file, "rb").read()
    st.audio(audio_bytes, format="audio/mp3")

    os.remove(audio_file)
