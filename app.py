import streamlit as st
from PIL import Image, ImageDraw
import asyncio
import edge_tts
import time
from mutagen.mp3 import MP3

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
    "Spanish": "es-ES-AlvaroNeural"
}

# -----------------------------
# FULL SPEECH PER LANGUAGE
# -----------------------------
texts = {
    "English": """GlobalInternet.py – Build with Python. Deliver with Speed.

We don’t just write code. We build complete, production-ready software on demand – tailored to your needs, delivered by email in record time.

What we do:
Custom web applications Streamlit Flask Django
Election and voting systems (like the one you just saw)
AI-powered tools chatbots data analysis automation
Business dashboards reporting tools internal workflows
Any Python-based project you can imagine – we make it work online

Who we are:
GlobalInternet.py was founded by Gesner Deslandes – owner, founder, and lead engineer.
Like Silicon Valley, but with a Haitian touch and outstanding outcomes.
We leverage AI and modern Python frameworks to build fast, reliable, and scalable solutions.

Our promise:
We are an online company working for the world.
No matter where you are, we deliver the full software package via email – ready to install and use.

Contact us right now
Phone / WhatsApp (509)-47385663
Email deslandes78@gmail.com

Whether you need a company website, a custom software tool, or a full-scale online platform – we build it, you own it.

GlobalInternet.py – Your Python partner, from Haiti to the world.""",

    "French": """Système de vote en ligne officiel prêt pour les élections en Haïti.
GlobalInternet.py, propriété de Gesner Deslandes...""",

    "Spanish": """Sistema oficial de votación en línea para elecciones en Haití.
Desarrollado por GlobalInternet.py..."""
}

# -----------------------------
# HUMANOID FACE
# -----------------------------
def create_face(mouth_open=False):
    img = Image.new("RGB", (400, 400), "white")
    draw = ImageDraw.Draw(img)

    # face
    draw.ellipse((50, 80, 350, 350), outline="black", width=5)
    draw.ellipse((90, 120, 310, 320), outline="black", width=4)

    # eyes
    draw.ellipse((140, 170, 180, 210), fill="black")
    draw.ellipse((220, 170, 260, 210), fill="black")

    # mouth
    if mouth_open:
        draw.ellipse((170, 240, 230, 300), outline="black", width=4)
    else:
        draw.arc((150, 230, 250, 300), start=0, end=180, fill="black", width=4)

    # antenna
    draw.line((200, 80, 200, 40), fill="black", width=4)
    draw.ellipse((185, 20, 215, 50), outline="black", width=3)

    # arms
    draw.rectangle((40, 180, 70, 260), outline="black", width=3)
    draw.rectangle((330, 180, 360, 260), outline="black", width=3)

    return img

# -----------------------------
# VOICE GENERATION
# -----------------------------
async def generate_voice(text, voice):
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save("voice.mp3")

# -----------------------------
# GET REAL AUDIO DURATION
# -----------------------------
def get_audio_duration(file_path):
    audio = MP3(file_path)
    return audio.info.length

# -----------------------------
# UI LAYOUT
# -----------------------------
left, right = st.columns([3, 1])

# -----------------------------
# RIGHT PANEL
# -----------------------------
with right:
    st.markdown("### 🏢 Company Info")

    st.markdown("**GlobalInternet.py**")
    st.markdown("Online Software Company")
    st.markdown("Owner: Gesner Deslandes")

    st.markdown("---")
    st.markdown("### 📞 Contact")

    st.markdown("📱 Phone: (509)-47385663")
    st.markdown("📧 Email: deslandes78@gmail.com")
    st.markdown("🏢 Office: Available upon request")

    st.markdown("---")
    st.info("AI & Software Solutions built in Haiti 🇭🇹")

# -----------------------------
# LEFT PANEL
# -----------------------------
with left:

    st.title("🤖 Gesner Humanoid AI")

    st.markdown(
        "<div style='text-align:center;'><img src='https://upload.wikimedia.org/wikipedia/commons/5/56/Flag_of_Haiti.svg' width='120'></div>",
        unsafe_allow_html=True
    )

    language = st.selectbox("🌍 Select Language", list(voices.keys()))

    frame = st.empty()
    frame.image(create_face(False))

    if st.button("▶️ Speak"):

        # generate voice
        asyncio.run(generate_voice(texts[language], voices[language]))

        audio_file = "voice.mp3"

        # play audio
        audio_bytes = open(audio_file, "rb").read()
        st.audio(audio_bytes, format="audio/mp3", autoplay=True)

        # 🔥 REAL DURATION FIX
        duration = get_audio_duration(audio_file)

        start = time.time()

        # 👄 LIPS SYNCHED TO REAL AUDIO TIME
        while time.time() - start < duration:
            frame.image(create_face(True))
            time.sleep(0.15)

            frame.image(create_face(False))
            time.sleep(0.15)

        frame.image(create_face(False))
