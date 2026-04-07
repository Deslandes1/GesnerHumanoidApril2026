import streamlit as st
from PIL import Image, ImageDraw
import asyncio
import edge_tts
import time

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(layout="wide")

# -----------------------------
# VOICE SETTINGS
# -----------------------------
voices = {
    "English": "en-US-GuyNeural",
    "French": "fr-FR-HenriNeural",
    "Spanish": "es-ES-AlvaroNeural",
    "Promo": "en-US-GuyNeural"
}

# -----------------------------
# DISPLAY TEXT (PRETTY UI VERSION)
# -----------------------------
display_texts = {
    "English": "Official Online Voting System for Haiti Elections...",
    "French": "Système de vote en ligne officiel prêt pour les élections en Haïti...",
    "Spanish": "Sistema oficial de votación en línea para elecciones en Haití...",

    "Promo": """
🚀 GlobalInternet.py – Build with Python. Deliver with Speed.

We don’t just write code. We build complete production-ready software on demand – tailored to your needs, delivered by email in record time.

💡 What we do:
- Custom web applications (Streamlit, Flask, Django)
- Election & voting systems
- AI-powered tools (chatbots, data analysis, automation)
- Business dashboards and workflows
- Any Python-based project you can imagine

👨‍💻 Who we are:
GlobalInternet.py was founded by Gesner Deslandes – owner, founder, and lead engineer.
Like Silicon Valley, but with a Haitian touch and outstanding outcomes.

🌍 Our promise:
We are an online company working for the world.
We deliver full software packages by email, ready to install and use.

📞 Contact:
Phone/WhatsApp: (509)-47385663
Email: deslandes78@gmail.com

GlobalInternet.py – Your Python partner from Haiti to the world. 🇭🇹
"""
}

# -----------------------------
# SPEECH TEXT (CLEAN VERSION FOR TTS)
# -----------------------------
speech_texts = {
    "English": display_texts["English"],
    "French": display_texts["French"],
    "Spanish": display_texts["Spanish"],

    "Promo": """
GlobalInternet py Build with Python Deliver with Speed.

We don’t just write code. We build complete production ready software on demand tailored to your needs delivered by email in record time.

What we do.

Custom web applications using Streamlit Flask and Django.
Election and voting systems.
Artificial intelligence tools including chatbots data analysis and automation.
Business dashboards reporting tools and workflows.
Any Python based project you can imagine we make it work online.

Who we are.

GlobalInternet py was founded by Gesner Deslandes owner founder and lead engineer.
Like Silicon Valley but with a Haitian touch and strong results.

Our promise.

We are an online company working for the world.
We deliver full software packages by email ready to install and use.

Contact us.

Phone or WhatsApp five zero nine four seven three eight five six six three.
Email deslandes78 at gmail dot com.

GlobalInternet py your Python partner from Haiti to the world.
"""
}

# -----------------------------
# HUMANOID FACE
# -----------------------------
def create_face(mouth_open=False):
    img = Image.new("RGB", (400, 400), "white")
    draw = ImageDraw.Draw(img)

    draw.ellipse((50, 80, 350, 350), outline="black", width=5)
    draw.ellipse((90, 120, 310, 320), outline="black", width=4)

    draw.ellipse((140, 170, 180, 210), fill="black")
    draw.ellipse((220, 170, 260, 210), fill="black")

    if mouth_open:
        draw.ellipse((170, 240, 230, 300), outline="black", width=4)
    else:
        draw.arc((150, 230, 250, 300), start=0, end=180, fill="black", width=4)

    draw.line((200, 80, 200, 40), fill="black", width=4)
    draw.ellipse((185, 20, 215, 50), outline="black", width=3)

    draw.rectangle((40, 180, 70, 260), outline="black", width=3)
    draw.rectangle((330, 180, 360, 260), outline="black", width=3)

    return img

# -----------------------------
# VOICE GENERATION
# -----------------------------
async def generate_voice(text, voice):
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save("voice.mp3")

def estimate_duration(text):
    return len(text.split()) / 2.5

# -----------------------------
# UI LAYOUT
# -----------------------------
left, right = st.columns([3, 1])

# RIGHT PANEL
with right:
    st.markdown("### 🏢 GlobalInternet.py")
    st.markdown("Owner: Gesner Deslandes")
    st.markdown("Online Software Company")

    st.markdown("---")
    st.markdown("### 📞 Contact")
    st.markdown("📱 (509)-47385663")
    st.markdown("📧 deslandes78@gmail.com")

    st.info("AI Software Built in Haiti 🇭🇹")

# LEFT PANEL
with left:

    st.title("🤖 Gesner Humanoid AI")

    st.markdown(
        "<div style='text-align:center;'><img src='https://upload.wikimedia.org/wikipedia/commons/5/56/Flag_of_Haiti.svg' width='120'></div>",
        unsafe_allow_html=True
    )

    mode = st.selectbox("🌍 Select Mode", list(voices.keys()))

    frame = st.empty()
    frame.image(create_face(False))

    # SHOW TEXT
    st.markdown("### 📜 Script Preview")
    st.write(display_texts[mode])

    if st.button("▶️ Speak"):

        asyncio.run(generate_voice(speech_texts[mode], voices[mode]))

        audio_file = open("voice.mp3", "rb")
        st.audio(audio_file.read(), format="audio/mp3")

        duration = estimate_duration(speech_texts[mode])

        start = time.time()
        while time.time() - start < duration:
            frame.image(create_face(True))
            time.sleep(0.2)
            frame.image(create_face(False))
            time.sleep(0.2)

        frame.image(create_face(False))
