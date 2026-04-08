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
# WEBSITE PROMOTION SCRIPT
# -----------------------------
texts = {

    "English": """Welcome to GlobalInternet.py.

This is Gesner Deslandes, owner of an online software company based in Haiti.

We are proud to introduce our official website.

Visit now:
globalinternetsitepy dash abh7v6tnmskxxnuplrdcgk dot streamlit dot app.

On our website, you will discover our services, our projects, and powerful software solutions built with Python and artificial intelligence.

We build complete software systems and deliver them directly to you by email within twenty four hours.

If you need a website, a custom application, or any software solution, contact us now.

Phone: five zero nine, four seven three, eight five six six three.

Email: deslandes seventy eight at gmail dot com.

GlobalInternet.py, your online software company, building solutions for the world from Haiti.""",

    "French": """Bienvenue sur GlobalInternet.py.

Je suis Gesner Deslandes, propriétaire d'une entreprise de logiciels en ligne basée en Haïti.

Nous sommes fiers de vous présenter notre site officiel.

Visitez maintenant :
globalinternetsitepy tiret abh7v6tnmskxxnuplrdcgk point streamlit point app.

Sur notre site, vous découvrirez nos services, nos projets et des solutions puissantes basées sur Python et l’intelligence artificielle.

Nous créons des logiciels complets et les livrons par email en vingt-quatre heures.

Si vous avez besoin d’un site web ou d’un logiciel personnalisé, contactez-nous.

Téléphone : cinq zéro neuf, quatre sept trois, huit cinq six six trois.

Email : deslandes soixante-dix-huit arrobase gmail point com.

GlobalInternet.py, votre entreprise de logiciels en ligne depuis Haïti vers le monde.""",

    "Spanish": """Bienvenido a GlobalInternet.py.

Soy Gesner Deslandes, propietario de una empresa de software en línea en Haití.

Estamos orgullosos de presentar nuestro sitio web oficial.

Visita ahora:
globalinternetsitepy guion abh7v6tnmskxxnuplrdcgk punto streamlit punto app.

En nuestro sitio encontrarás servicios, proyectos y soluciones de software con Python e inteligencia artificial.

Creamos software completo y lo entregamos por correo electrónico en veinticuatro horas.

Si necesitas un sitio web o una aplicación personalizada, contáctanos.

Teléfono: cinco cero nueve, cuatro siete tres, ocho cinco seis seis tres.

Correo: deslandes setenta y ocho arroba gmail punto com.

GlobalInternet.py, tu empresa de software en línea desde Haití para el mundo."""
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

def get_audio_duration(file_path):
    return MP3(file_path).info.length

# -----------------------------
# UI
# -----------------------------
left, right = st.columns([3, 1])

# RIGHT PANEL
with right:
    st.markdown("## 🌐 GlobalInternet.py")
    st.markdown("Owner: Gesner Deslandes")
    st.markdown("📱 (509)-47385663")
    st.markdown("📧 deslandes78@gmail.com")
    st.markdown("---")
    st.success("Visit our website")

# LEFT PANEL
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

        asyncio.run(generate_voice(texts[language], voices[language]))

        audio_file = "voice.mp3"
        st.audio(open(audio_file, "rb").read(), autoplay=True)

        duration = get_audio_duration(audio_file)
        start = time.time()

        mouth = False
        while time.time() - start < duration:
            mouth = not mouth
            frame.image(create_face(mouth))
            time.sleep(0.12)

        frame.image(create_face(False))
