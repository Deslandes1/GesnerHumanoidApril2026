import streamlit as st
from PIL import Image, ImageDraw
import asyncio
import edge_tts
import time
from mutagen.mp3 import MP3
import base64
import os
import tempfile

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(layout="wide", page_title="Gesner Humanoid AI")

# -----------------------------
# VOICES & TEXTS (SENDWAVE SCRIPT)
# -----------------------------
voices = {
    "English": "en-US-GuyNeural",
    "French": "fr-FR-HenriNeural",
    "Spanish": "es-ES-AlvaroNeural"
}

sendwave_script = """Hello, I am the Gesner Humanoid AI. Family is everything, and today, I will explain how your relatives and friends abroad can send support to Haiti instantly using Sendwave. Sendwave is a secure mobile app built for international money transfers with very low fees. Here is how it works: Your family member in the USA, Canada, or Europe downloads the Sendwave app and links their debit card. Then, they simply select Haiti, enter your phone number, and choose how you will receive the funds. They can send the money directly to your Moncash wallet, your Natcash account, or for cash pickup at a trusted local agent. The transfer is completed within seconds, and the money is ready for you to use. It is that simple, fast, and secure. This was Gesner Deslandes, explaining to you how this international money transfer works to keep us connected. Thank you."""

texts = {
    "English": sendwave_script,
    "French": """Bonjour, je suis l'IA Humanoïde Gesner. La famille est tout, et aujourd'hui, j'expliquerai comment vos parents et amis à l'étranger peuvent envoyer un soutien instantané en Haïti en utilisant Sendwave. C'était Gesner Deslandes, vous expliquant comment fonctionne ce transfert d'argent international.""",
    "Spanish": """Hola, soy la IA Humanoide de Gesner. La familia lo es todo, y hoy explicaré cómo sus familiares y amigos en el extranjero pueden enviar apoyo instantáneo a Haití usando Sendwave. Este fue Gesner Deslandes, explicándole cómo funciona esta transferencia internacional de dinero."""
}

# -----------------------------
# FACE DESIGN
# -----------------------------
def create_face(is_open=False):
    img = Image.new("RGB", (400, 400), "white")
    draw = ImageDraw.Draw(img)

    # Face Shape
    draw.ellipse((50, 80, 350, 350), outline="black", width=5)
    draw.ellipse((90, 120, 310, 320), outline="black", width=3)
    
    # Eyes
    draw.ellipse((140, 170, 180, 210), fill="black")
    draw.ellipse((220, 170, 260, 210), fill="black")

    # Aggressive Mouth Movement
    center_y = 265
    if is_open:
        draw.ellipse((140, center_y - 30, 260, center_y + 30), fill="black")
    else:
        draw.line((150, center_y, 250, center_y), fill="black", width=12)

    # Robot Antenna
    draw.line((200, 40, 200, 80), fill="black", width=4)
    draw.ellipse((185, 20, 215, 50), outline="black", width=3)
    
    return img

# -----------------------------
# UI LAYOUT
# -----------------------------
left, right = st.columns([3, 1])

with right:
    # BLUE SENDWAVE TEXT REPLACING LOGO
    st.markdown("""
        <div style="text-align: center; padding: 10px;">
            <h1 style="color: #1a73e8; font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; font-size: 42px; font-weight: bold; letter-spacing: -1px;">
                SendWave
            </h1>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    # BEAUTIFIED COMPANY NAME
    st.markdown("""
        <div style="background-color: #f0f2f6; padding: 15px; border-radius: 8px;">
            <h3 style="color: #003366; margin: 0;">GlobalInternet.py</h3>
            <p style="font-size: 0.8em; color: #555;">Fast Software Solutions</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("**Owner:** Gesner Deslandes")
    st.markdown("📱 (509)-47385663")
    st.markdown("📧 deslandes78@gmail.com")
    st.success("Haiti Global Support 🇭🇹")

with left:
    st.title("🤖 Gesner Humanoid AI")
    
    # HAITIAN FLAG
    st.markdown(
        "<div style='text-align:center;'><img src='https://upload.wikimedia.org/wikipedia/commons/5/56/Flag_of_Haiti.svg' width='120'></div>",
        unsafe_allow_html=True
    )
    
    language = st.selectbox("🌍 Select Language", list(voices.keys()))
    
    face_placeholder = st.empty()
    face_placeholder.image(create_face(is_open=False))

    if st.button("▶️ Start Presentation"):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
            audio_path = tmp.name

        with st.spinner("Preparing Audio..."):
            asyncio.run(edge_tts.Communicate(texts[language], voices[language]).save(audio_path))

        with open(audio_path, "rb") as f:
            b64 = base64.b64encode(f.read()).decode()
        
        duration = MP3(audio_path).info.length
        st.markdown(f'<audio autoplay><source src="data:audio/mp3;base64,{b64}" type="audio/mp3"></audio>', unsafe_allow_html=True)
        
        # SYNCED ANIMATION
        start_time = time.time()
        toggle = True
        while (time.time() - start_time) < duration:
            face_placeholder.image(create_face(is_open=toggle))
            toggle = not toggle
            time.sleep(0.05)
        
        face_placeholder.image(create_face(is_open=False))
        
        if os.path.exists(audio_path):
            os.remove(audio_path)
