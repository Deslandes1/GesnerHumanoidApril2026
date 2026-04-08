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
# FACE DESIGN (REAL TALKING LIPS)
# -----------------------------
def create_face(mouth_val=0.0):
    """
    mouth_val: 0.0 (closed) to 1.0 (fully open)
    """
    img = Image.new("RGB", (400, 400), "white")
    draw = ImageDraw.Draw(img)

    # Face Outlines
    draw.ellipse((50, 80, 350, 350), outline="black", width=5)
    draw.ellipse((90, 120, 310, 320), outline="black", width=3)
    
    # Eyes
    draw.ellipse((140, 170, 180, 210), fill="black")
    draw.ellipse((220, 170, 260, 210), fill="black")

    # --- THE TALKING LIPS ---
    center_y = 265
    # Mouth expands both UP and DOWN from the center line
    half_height = 2 + (mouth_val * 25) 
    
    y0 = center_y - half_height
    y1 = center_y + half_height
    
    # Draw the animated lips (Oval that grows/shrinks)
    draw.ellipse((160, y0, 240, y1), outline="black", width=6)

    # Robot details
    draw.line((200, 80, 200, 40), fill="black", width=4)
    draw.ellipse((185, 20, 215, 50), outline="black", width=3)
    draw.rectangle((40, 180, 70, 260), outline="black", width=3)
    draw.rectangle((330, 180, 360, 260), outline="black", width=3)

    return img

# -----------------------------
# VOICE ENGINE
# -----------------------------
async def generate_voice(text, voice, path):
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(path)

# -----------------------------
# UI STRUCTURE
# -----------------------------
left, right = st.columns([3, 1])

with right:
    st.markdown("## 🌐 GlobalInternet.py")
    st.markdown("**Owner:** Gesner Deslandes")
    st.markdown("📱 (509)-47385663")
    st.markdown("📧 deslandes78@gmail.com")
    st.markdown("🔗 [Main Website](https://globalinternetsitepy-abh7v6tnmskxxnuplrdcgk.streamlit.app/)")
    st.markdown("---")
    st.success("AI & Software Solutions 🇭🇹")

with left:
    st.title("🤖 Gesner Humanoid AI")
    
    # RESTORED HAITIAN FLAG
    st.markdown(
        "<div style='text-align:center;'><img src='https://upload.wikimedia.org/wikipedia/commons/5/56/Flag_of_Haiti.svg' width='120'></div>",
        unsafe_allow_html=True
    )
    
    language = st.selectbox("🌍 Select Language", list(voices.keys()))
    
    # The placeholder for the robot face
    face_placeholder = st.empty()
    face_placeholder.image(create_face(0.0))

    if st.button("▶️ Start Speaking"):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
            audio_path = tmp.name

        with st.spinner("Gesner AI is preparing to speak..."):
            asyncio.run(generate_voice(texts[language], voices[language], audio_path))

        # Audio Autoplay
        with open(audio_path, "rb") as f:
            audio_bytes = f.read()
            b64_audio = base64.b64encode(audio_bytes).decode()
            st.markdown(
                f'<audio autoplay><source src="data:audio/mp3;base64,{b64_audio}" type="audio/mp3"></audio>', 
                unsafe_allow_html=True
            )

        # Exact Duration
        duration = MP3(audio_path).info.length
        
        # --- IMPROVED TALKING ANIMATION ---
        start_time = time.time()
        while (time.time() - start_time) < duration:
            elapsed = time.time() - start_time
            
            # Complex wave for more natural "speech" movement
            # Mixing two frequencies (15 and 30) makes it look less like a robot and more like talking
            wave = (math.sin(elapsed * 15) * 0.5) + (math.sin(elapsed * 30) * 0.5)
            mouth_pos = abs(wave)
            
            face_placeholder.image(create_face(mouth_pos))
            
            # Keep the refresh rate high (approx 25 frames per second)
            time.sleep(0.04)

        # Reset to closed mouth
        face_placeholder.image(create_face(0.0))
        
        # Clean up
        if os.path.exists(audio_path):
            os.remove(audio_path)
