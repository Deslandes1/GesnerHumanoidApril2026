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
# YOUR SCRIPT (KEEP AS YOU WANT)
# -----------------------------
texts = {
    "English": """Welcome to GlobalInternet.py.
Visit our official website:
https://globalinternetsitepy-abh7v6tnmskxxnuplrdcgk.streamlit.app/
We build software and deliver it in 24 hours.
Contact us now.
Phone: (509)-47385663
Email: deslandes78@gmail.com""",

    "French": """Bienvenue sur GlobalInternet.py.
Visitez notre site officiel:
https://globalinternetsitepy-abh7v6tnmskxxnuplrdcgk.streamlit.app/
Nous livrons des logiciels en 24 heures.
Contactez-nous.""",

    "Spanish": """Bienvenido a GlobalInternet.py.
Visita nuestro sitio web:
https://globalinternetsitepy-abh7v6tnmskxxnuplrdcgk.streamlit.app/
Entregamos software en 24 horas.
Contáctanos."""
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
    frame.image(create_face(False))

    # ✅ BUTTON BACK
    if st.button("▶️ Speak"):

        # Generate voice
        asyncio.run(generate_voice(texts[language], voices[language]))

        audio_file = "voice.mp3"

        # ✅ NORMAL AUDIO (VISIBLE PLAYER)
        st.audio(open(audio_file, "rb").read(), format="audio/mp3")

        # ✅ REAL DURATION
        duration = get_audio_duration(audio_file)

        # 🔥 MOUTH MOVES UNTIL END
        start = time.time()
        mouth = False

        while time.time() - start < duration:
            mouth = not mouth
            frame.image(create_face(mouth))
            time.sleep(0.1)

        frame.image(create_face(False))
