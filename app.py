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
# FACE DESIGN (MOUTH ANIMATION)
# -----------------------------
def create_face(mouth_open=0.0):
    img = Image.new("RGB", (400, 400), "white")
    draw = ImageDraw.Draw(img)

    # Face Outlines
    draw.ellipse((50, 80, 350, 350), outline="black", width=5)
    draw.ellipse((90, 120, 310, 320), outline="black", width=3)
    
    # Eyes
    draw.ellipse((140, 170, 180, 210), fill="black")
    draw.ellipse((220, 170, 260, 210), fill="black")

    # --- THE MOUTH ---
    # Top of the mouth is fixed at 255
    y_top = 255
    # The bottom moves based on mouth_open (val between 0 and 1)
    # We ensure y_bottom is always at least 5 pixels below y_top
    y_bottom = y_top + 5 + int(mouth_open * 55)
    
    # Draw the animated lips
    draw.ellipse((165, y_top, 235, y_bottom), outline="black", width=5)

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
    
    language = st.selectbox("🌍 Select Language", list(voices.keys()))
    
    # The placeholder for the robot face
    face_placeholder = st.empty()
    face_placeholder.image(create_face(0.0))

    if st.button("▶️ Start Speaking"):
        # Create temporary audio storage
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
            audio_path = tmp.name

        with st.spinner("Gesner AI is thinking..."):
            asyncio.run(generate_voice(texts[language], voices[language], audio_path))

        # Play audio immediately
        with open(audio_path, "rb") as f:
            audio_bytes = f.read()
            b64_audio = base64.b64encode(audio_bytes).decode()
            st.markdown(
                f'<audio autoplay><source src="data:audio/mp3;base64,{b64_audio}" type="audio/mp3"></audio>', 
                unsafe_allow_html=True
            )

        # Calculate exact duration
        audio_info = MP3(audio_path)
        duration = audio_info.info.length
        
        # --- SUSTAINED ANIMATION LOOP ---
        start_time = time.time()
        while (time.time() - start_time) < duration:
            current_elapsed = time.time() - start_time
            
            # Using absolute sine for high-speed mouth chatter (up and down)
            # Speed is set to 20 for a very responsive look
            mouth_pos = abs(math.sin(current_elapsed * 20))
            
            # Re-render face with the new mouth position
            face_placeholder.image(create_face(mouth_pos))
            
            # Frame rate control
            time.sleep(0.04)

        # Close the mouth completely once audio is done
        face_placeholder.image(create_face(0.0))
        
        # Clean up the file system
        if os.path.exists(audio_path):
            os.remove(audio_path)
