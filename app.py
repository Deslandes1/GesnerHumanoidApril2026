import streamlit as st
from PIL import Image, ImageDraw
import asyncio
import edge_tts
import time
from mutagen.mp3 import MP3
import base64
import os
import math
import tempfile

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(layout="wide", page_title="Gesner Humanoid AI")

# -----------------------------
# VOICES & TEXTS
# -----------------------------
voices = {
    "English": "en-US-GuyNeural",
    "French": "fr-FR-HenriNeural",
    "Spanish": "es-ES-AlvaroNeural"
}

texts = {
    "English": "Discover GlobalInternet.py – Your Python Software Partner. https://globalinternetsitepy-abh7v6tnmskxxnuplrdcgk.streamlit.app/ We build software and deliver it in 24 hours. Phone: (509)-47385663 Email: deslandes78@gmail.com",
    "French": "Découvrez GlobalInternet.py – votre partenaire logiciel Python. https://globalinternetsitepy-abh7v6tnmskxxnuplrdcgk.streamlit.app/ Nous développons des logiciels livrés en 24 heures. Téléphone: (509)-47385663 Email: deslandes78@gmail.com",
    "Spanish": "Descubre GlobalInternet.py – tu socio de software en Python. https://globalinternetsitepy-abh7v6tnmskxxnuplrdcgk.streamlit.app/ Creamos software y lo entregamos en 24 horas. Teléfono: (509)-47385663 Correo: deslandes78@gmail.com"
}

# -----------------------------
# FACE DESIGN (LIPS FIXED)
# -----------------------------
def create_face(mouth_open=0.0):
    # Canvas
    img = Image.new("RGB", (400, 400), "white")
    draw = ImageDraw.Draw(img)

    # Face Shape
    draw.ellipse((50, 80, 350, 350), outline="black", width=5)
    draw.ellipse((90, 120, 310, 320), outline="black", width=3)
    
    # Eyes
    draw.ellipse((140, 170, 180, 210), fill="black")
    draw.ellipse((220, 170, 260, 210), fill="black")

    # --- MOUTH LOGIC (Safety Check for PIL) ---
    y0 = 260
    # Ensure y1 is ALWAYS >= y0 to prevent ValueError
    y1 = y0 + max(2, int(mouth_open * 50))
    
    # Draw talking lips
    draw.ellipse((160, y0, 240, y1), outline="black", width=4)

    # Antenna & Decoration
    draw.line((200, 80, 200, 40), fill="black", width=4)
    draw.ellipse((185, 20, 215, 50), outline="black", width=3)
    
    return img

# -----------------------------
# ASYNC VOICE GENERATION
# -----------------------------
async def generate_voice(text, voice, path):
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(path)

# -----------------------------
# UI LAYOUT
# -----------------------------
left, right = st.columns([3, 1])

with right:
    st.markdown("## 🌐 GlobalInternet.py")
    st.markdown("**Owner:** Gesner Deslandes")
    st.markdown("📱 (509)-47385663")
    st.markdown("📧 deslandes78@gmail.com")
    st.info("AI & Software Solutions 🇭🇹")

with left:
    st.title("🤖 Gesner Humanoid AI")
    language = st.selectbox("🌍 Select Language", list(voices.keys()))
    
    # Image Placeholder
    frame = st.empty()
    frame.image(create_face(0))

    if st.button("▶️ Speak"):
        # Create temp file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
            audio_path = tmp.name

        with st.spinner("Generating..."):
            asyncio.run(generate_voice(texts[language], voices[language], audio_path))

        # Audio Playback
        with open(audio_path, "rb") as f:
            data = f.read()
            b64 = base64.b64encode(data).decode()
            st.markdown(f'<audio autoplay><source src="data:audio/mp3;base64,{b64}" type="audio/mp3"></audio>', unsafe_allow_html=True)

        # Animation Timing
        audio = MP3(audio_path)
        duration = audio.info.length
        start_time = time.time()

        # Animation Loop
        while time.time() - start_time < duration:
            elapsed = time.time() - start_time
            # Sin wave for the "Lips" movement
            val = abs(math.sin(elapsed * 15)) 
            frame.image(create_face(val))
            time.sleep(0.05)

        # Reset mouth
        frame.image(create_face(0))
        
        # Cleanup file
        os.remove(audio_path)
