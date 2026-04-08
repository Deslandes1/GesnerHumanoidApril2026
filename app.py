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
# SCRIPT
# -----------------------------
texts = {
    "English": """Welcome to GlobalInternet.py.
This is Gesner Deslandes, owner of an online software company based in Haiti.
Visit our official website now.
globalinternetsitepy dash abh7v6tnmskxxnuplrdcgk dot streamlit dot app.
We build and deliver complete software solutions within 24 hours.
Contact us today.
Phone: five zero nine, four seven three, eight five six six three.
Email: deslandes seventy eight at gmail dot com.
GlobalInternet.py, building software for the world.""",

    "French": """Bienvenue sur GlobalInternet.py.
Je suis Gesner Deslandes, propriétaire d’une entreprise de logiciels en ligne.
Visitez notre site officiel maintenant.
globalinternetsitepy tiret abh7v6tnmskxxnuplrdcgk point streamlit point app.
Nous livrons des logiciels complets en 24 heures.
Contactez-nous dès aujourd’hui.""",

    "Spanish": """Bienvenido a GlobalInternet.py.
Soy Gesner Deslandes, propietario de una empresa de software en línea.
Visita nuestro sitio web ahora.
globalinternetsitepy guion abh7v6tnmskxxnuplrdcgk punto streamlit punto app.
Entregamos software completo en 24 horas.
Contáctanos hoy."""
}

# -----------------------------
# FACE
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
# VOICE
# -----------------------------
async def generate_voice(text, voice):
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save("voice.mp3")

def get_audio_duration(file):
    return MP3(file).info.length

# -----------------------------
# UI
# -----------------------------
left, right = st.columns([3, 1])

with right:
    st.markdown("## 🌐 GlobalInternet.py")
    st.markdown("Gesner Deslandes")
    st.markdown("📱 (509)-47385663")
    st.markdown("📧 deslandes78@gmail.com")

with left:

    st.title("🤖 Gesner Humanoid AI")

    st.markdown(
        "<div style='text-align:center;'><img src='https://upload.wikimedia.org/wikipedia/commons/5/56/Flag_of_Haiti.svg' width='120'></div>",
        unsafe_allow_html=True
    )

    language = st.selectbox("🌍 Select Language", list(voices.keys()))

    frame = st.empty()

    # initial face
    frame.image(create_face(False))

    if st.button("▶️ Speak"):

        # generate voice
        asyncio.run(generate_voice(texts[language], voices[language]))

        audio_file = "voice.mp3"

        # get duration
        duration = get_audio_duration(audio_file)

        # play audio (non-blocking)
        st.markdown(
            f"""
            <audio autoplay>
            <source src="data:audio/mp3;base64,{open(audio_file, "rb").read().hex()}">
            </audio>
            """,
            unsafe_allow_html=True
        )

        # 🔥 FORCE LIVE ANIMATION
        start = time.time()
        mouth = False

        while time.time() - start < duration:
            mouth = not mouth
            frame.image(create_face(mouth))
            time.sleep(0.1)

        frame.image(create_face(False))
