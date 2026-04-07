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
# SPEECH TEXT (SHORTENED FORMAT SAFE FOR STREAMLIT)
# -----------------------------
english_text = (
"GlobalInternet.py – Build with Python. Deliver with Speed. "
"We build complete production-ready software delivered within 24 hours. "
"After your order, we send you an email with a zip file containing app.py, requirements, and a guide. "
"Download, extract, install requirements, and run using Streamlit or Python. "
"You can upload to GitHub and use Streamlit Cloud to access it anywhere. "
"You can store passwords securely using Streamlit secrets. "
"Contact us now if you need a website or custom software. "
"We build based on your needs and integrate your company logo professionally. "
"GlobalInternet.py – Your Python partner from Haiti to the world."
)

french_text = (
"GlobalInternet.py – Construisez avec Python. Livrez avec rapidité. "
"Nous créons des logiciels complets livrés en moins de 24 heures. "
"Après votre commande, nous envoyons un email avec un fichier zip contenant app.py, les dépendances et un guide. "
"Téléchargez, extrayez, installez et exécutez avec Streamlit ou Python. "
"Vous pouvez utiliser GitHub et Streamlit Cloud pour l'accès en ligne. "
"Utilisez les secrets Streamlit pour sécuriser vos mots de passe. "
"Contactez-nous pour un site web ou logiciel personnalisé. "
"Nous intégrons aussi votre logo professionnellement."
)

spanish_text = (
"GlobalInternet.py – Construye con Python. Entrega con rapidez. "
"Creamos software completo entregado en 24 horas. "
"Recibirás un email con un archivo zip que contiene app.py, dependencias y guía. "
"Descarga, extrae, instala y ejecuta con Streamlit o Python. "
"Puedes usar GitHub y Streamlit Cloud para acceso en línea. "
"Guarda contraseñas con seguridad usando Streamlit secrets. "
"Contáctanos para crear tu sitio web o software personalizado. "
"Integramos tu logo profesionalmente."
)

texts = {
    "English": english_text,
    "French": french_text,
    "Spanish": spanish_text
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
# LAYOUT FIX (CRITICAL)
# -----------------------------
col1, col2 = st.columns([2.8, 1.2], gap="large")

# -----------------------------
# RIGHT PANEL (LOCKED)
# -----------------------------
with col2:
    st.markdown("### 🏢 Company Info")
    st.markdown("**GlobalInternet.py**")
    st.markdown("Owner: Gesner Deslandes")

    st.markdown("---")
    st.markdown("📱 (509)-47385663")
    st.markdown("📧 deslandes78@gmail.com")

    st.markdown("---")
    st.success("Always available for projects")

# -----------------------------
# LEFT PANEL
# -----------------------------
with col1:

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

        while time.time() - start < duration:
            frame.image(create_face(True))
            time.sleep(0.15)
            frame.image(create_face(False))
            time.sleep(0.15)

        frame.image(create_face(False))
