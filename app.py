import streamlit as st
from PIL import Image, ImageDraw
import asyncio
import edge_tts
import time
from mutagen.mp3 import MP3
import base64
import random

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
# YOUR SCRIPT
# -----------------------------
texts = {
    "English": """Discover GlobalInternet.py – Your Python Software Partner.
Visit our official website:
https://globalinternetsitepy-abh7v6tnmskxxnuplrdcgk.streamlit.app/
We build software and deliver it in 24 hours.
Contact us now.
Phone: (509)-47385663
Email: deslandes78@gmail.com
GlobalInternet.py – Your Python partner from Haiti to the world.""",

    "French": """Découvrez GlobalInternet.py – votre partenaire logiciel Python.
Visitez notre site officiel:
https://globalinternetsitepy-abh7v6tnmskxxnuplrdcgk.streamlit.app/
Nous développons des logiciels livrés en 24 heures.
Contactez-nous maintenant.
Téléphone: (509)-47385663
Email: deslandes78@gmail.com""",

    "Spanish": """Descubre GlobalInternet.py – tu socio de software en Python.
Visita nuestro sitio web:
https://globalinternetsitepy-abh7v6tnmskxxnuplrdcgk.streamlit.app/
Creamos software y lo entregamos en 24 horas.
Contáctanos ahora.
Teléfono: (509)-47385663
Correo: deslandes78@gmail.com"""
}

# -----------------------------
# HUMANOID FACE (REALISTIC MOUTH)
# -----------------------------
def create_face(mouth_level=0):
    img = Image.new("RGB", (400, 400), "white")
    draw = ImageDraw.Draw(img)

    # Head
    draw.ellipse((50, 80, 350, 350), outline="black", width=5)
    draw.ellipse((90, 120, 310, 320), outline="black", width=4)

    # Eyes
    draw.ellipse((140, 170, 180, 210), fill="black")
    draw.ellipse((220, 170, 260, 210), fill="black")

    # 🔥 REALISTIC MOUTH (VARIABLE OPENING)
    top = 240
    bottom = 240 + int(20 + mouth_level * 40)

    draw.ellipse((170, top, 230, bottom), outline="black", width=4)

    # Antenna
    draw.line((200, 80, 200, 40), fill="black", width=4)
    draw.ellipse((185, 20, 215, 50), outline="black", width=3)

    # Side panels
    draw.rectangle((40, 180, 70, 260), outline="black", width=3)
    draw.rectangle((330, 180, 360, 260), outline="black", width=3)

    return img

# -----------------------------
# GENERATE VOICE
# -----------------------------
async def generate_voice(text, voice):
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save("voice.mp3")

# -----------------------------
# UI LAYOUT
# -----------------------------
left, right = st.columns([3, 1])

# -----------------------------
# RIGHT PANEL (UNCHANGED)
# -----------------------------
with right:
    st.markdown("## 🌐 GlobalInternet.py")
    st.markdown("Owner: Gesner Deslandes")
    st.markdown("📱 (509)-47385663")
    st.markdown("📧 deslandes78@gmail.com")
    st.markdown("🔗 https://globalinternetsitepy-abh7v6tnmskxxnuplrdcgk.streamlit.app/")
    st.markdown("---")
    st.success("AI & Software Solutions 🇭🇹")

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
    frame.image(create_face(0))

    if st.button("▶️ Speak"):

        asyncio.run(generate_voice(texts[language], voices[language]))

        audio_file = "voice.mp3"

        # 🔥 AUTO PLAY
        with open(audio_file, "rb") as f:
            audio_bytes = f.read()
        audio_base64 = base64.b64encode(audio_bytes).decode()

        st.markdown(
            f"""
            <audio autoplay>
            <source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3">
            </audio>
            """,
            unsafe_allow_html=True
        )

        # 🔥 REAL AUDIO LENGTH
        duration = MP3(audio_file).info.length

        # 🔥 NATURAL TALKING EFFECT
        start = time.time()

        while time.time() - start < duration:
            # random talking intensity (like real speech)
            mouth_level = random.uniform(0.1, 1.0)

            frame.image(create_face(mouth_level))

            # variable speed (speech rhythm)
            time.sleep(random.uniform(0.05, 0.12))

        frame.image(create_face(0))
