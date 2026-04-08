import streamlit as st
from PIL import Image, ImageDraw
import edge_tts
import time
import base64
import math
import threading
import tempfile
import os
from mutagen.mp3 import MP3
import asyncio

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(layout="wide")

# -----------------------------
# VOICES
# -----------------------------
voices = {
    "English": "en-US-GuyNeural",
    "French": "fr-FR-HenriNeural",
    "Spanish": "es-ES-AlvaroNeural"
}

# -----------------------------
# TEXTS (Restored with your full details)
# -----------------------------
texts = {
    "English": """Discover GlobalInternet.py – Your Python Software Partner.
https://globalinternetsitepy-abh7v6tnmskxxnuplrdcgk.streamlit.app/
We build software and deliver it in 24 hours.
Phone: (509)-47385663
Email: deslandes78@gmail.com""",

    "French": """Découvrez GlobalInternet.py – votre partenaire logiciel Python.
https://globalinternetsitepy-abh7v6tnmskxxnuplrdcgk.streamlit.app/
Nous développons des logiciels livrés en 24 heures.
Téléphone: (509)-47385663
Email: deslandes78@gmail.com""",

    "Spanish": """Descubre GlobalInternet.py – tu socio de software en Python.
https://globalinternetsitepy-abh7v6tnmskxxnuplrdcgk.streamlit.app/
Creamos software y lo entregamos en 24 horas.
Teléfono: (509)-47385663
Correo: deslandes78@gmail.com"""
}

# -----------------------------
# FACE DESIGN (Talking Lips Logic)
# -----------------------------
def create_face(mouth_open=0):
    img = Image.new("RGB", (400, 400), "white")
    draw = ImageDraw.Draw(img)

    # Face Shape
    draw.ellipse((50, 80, 350, 350), outline="black", width=5)
    draw.ellipse((90, 120, 310, 320), outline="black", width=3)
    
    # Eyes
    draw.ellipse((140, 170, 180, 210), fill="black")
    draw.ellipse((220, 170, 260, 210), fill="black")

    # --- ANIMATED MOUTH ---
    # The mouth expands vertically based on the mouth_open value
    mouth_height = 10 + (mouth_open * 50)
    draw.ellipse((170, 240, 230, 240 + mouth_height), outline="black", width=4)

    # Antenna & Ears
    draw.line((200, 80, 200, 40), fill="black", width=4)
    draw.ellipse((185, 20, 215, 50), outline="black", width=3)
    draw.rectangle((40, 180, 70, 260), outline="black", width=3)
    draw.rectangle((330, 180, 360, 260), outline="black", width=3)

    return img

# -----------------------------
# VOICE GENERATION
# -----------------------------
def generate_voice_thread(text, voice, audio_path):
    async def _generate():
        communicate = edge_tts.Communicate(text, voice)
        await communicate.save(audio_path)
    asyncio.run(_generate())

# -----------------------------
# LAYOUT
# -----------------------------
left, right = st.columns([3, 1])

with right:
    st.markdown("## 🌐 GlobalInternet.py")
    st.markdown("Owner: Gesner Deslandes")
    st.markdown("📱 (509)-47385663")
    st.markdown("📧 deslandes78@gmail.com")
    st.markdown("🔗 [Click here to visit site](https://globalinternetsitepy-abh7v6tnmskxxnuplrdcgk.streamlit.app/)")
    st.markdown("---")
    st.success("AI & Software Solutions 🇭🇹")

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
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
            audio_path = tmp.name

        with st.spinner("Generating voice..."):
            thread = threading.Thread(
                target=generate_voice_thread,
                args=(texts[language], voices[language], audio_path)
            )
            thread.start()
            thread.join()

        # Autoplay audio
        with open(audio_path, "rb") as f:
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

        # Get duration for the animation loop
        duration = MP3(audio_path).info.length

        # --- RE-BUILT ANIMATION LOOP ---
        start = time.time()
        while time.time() - start < duration:
            elapsed = time.time() - start
            # Fast sine wave for "talking" movement
            # We use abs() so the mouth value stays between 0 and 1
            mouth_val = abs(math.sin(elapsed * 12)) 
            
            frame.image(create_face(mouth_val))
            time.sleep(0.05) 

        # Close mouth at the end
        frame.image(create_face(0))

        # Cleanup
        if os.path.exists(audio_path):
            os.unlink(audio_path)
