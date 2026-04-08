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
# FACE DESIGN (LIPS FIXED & STABLE)
# -----------------------------
def create_face(mouth_open=0.0):
    # Create white canvas
    img = Image.new("RGB", (400, 400), "white")
    draw = ImageDraw.Draw(img)

    # Face Shape (Robot Head)
    draw.ellipse((50, 80, 350, 350), outline="black", width=5)
    draw.ellipse((90, 120, 310, 320), outline="black", width=3)
    
    # Eyes
    draw.ellipse((140, 170, 180, 210), fill="black")
    draw.ellipse((220, 170, 260, 210), fill="black")

    # --- MOUTH LOGIC (TALKING LIPS) ---
    # Fixed top position so it doesn't "jump"
    y0 = 260
    # y1 increases as mouth_open increases (0.0 to 1.0)
    # Adding max(2, ...) ensures y1 is always greater than y0
    y1 = y0 + max(5, int(mouth_open * 60))
    
    # Draw the mouth ellipse (the lips)
    draw.ellipse((160, y0, 240, y1), outline="black", width=5)

    # Antenna
    draw.line((200, 80, 200, 40), fill="black", width=4)
    draw.ellipse((185, 20, 215, 50), outline="black", width=3)
    
    # Ears
    draw.rectangle((40, 180, 70, 260), outline="black", width=3)
    draw.rectangle((330, 180, 360, 260), outline="black", width=3)

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
    st.markdown("🔗 [Main Website](https://globalinternetsitepy-abh7v6tnmskxxnuplrdcgk.streamlit.app/)")
    st.markdown("---")
    st.success("AI & Software Solutions 🇭🇹")

with left:
    st.title("🤖 Gesner Humanoid AI")
    # Flag removed as requested
    
    language = st.selectbox("🌍 Select Language", list(voices.keys()))
    
    # Initialize the image frame
    frame = st.empty()
    frame.image(create_face(0))

    if st.button("▶️ Start Talking"):
        # Create temp audio file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
            audio_path = tmp.name

        with st.spinner("Preparing response..."):
            # Run the voice generator
            asyncio.run(generate_voice(texts[language], voices[language], audio_path))

        # Encode audio to base64 for autoplay
        with open(audio_path, "rb") as f:
            data = f.read()
            b64 = base64.b64encode(data).decode()
            st.markdown(
                f'<audio autoplay><source src="data:audio/mp3;base64,{b64}" type="audio/mp3"></audio>', 
                unsafe_allow_html=True
            )

        # Get audio length using mutagen
        audio = MP3(audio_path)
        duration = audio.info.length
        start_time = time.time()

        # --- ANIMATION LOOP ---
        while time.time() - start_time < duration:
            elapsed = time.time() - start_time
            # Create a rhythmic "up and down" motion for the lips
            # val goes from 0 to 1 based on sine wave
            val = abs(math.sin(elapsed * 18)) 
            
            # Update the robot face image
            frame.image(create_face(val))
            
            # Control the frame rate (approx 20 FPS)
            time.sleep(0.05)

        # Ensure mouth is closed when done
        frame.image(create_face(0))
        
        # Delete temp file
        if os.path.exists(audio_path):
            os.remove(audio_path)
