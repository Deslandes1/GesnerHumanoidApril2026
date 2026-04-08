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
st.set_page_config(page_title="Gesner Humanoid AI", layout="wide")

# -----------------------------
# VOICES & TEXTS
# -----------------------------
voices = {
    "English": "en-US-GuyNeural",
    "French": "fr-FR-HenriNeural",
    "Spanish": "es-ES-AlvaroNeural"
}

texts = {
    "English": "Discover GlobalInternet.py – Your Python Software Partner. We build software and deliver it in 24 hours.",
    "French": "Découvrez GlobalInternet.py – votre partenaire logiciel Python. Nous développons des logiciels livrés en 24 heures.",
    "Spanish": "Descubre GlobalInternet.py – tu socio de software en Python. Creamos software y lo entregamos en 24 horas."
}

# -----------------------------
# FACE DESIGN (The "Lips" Logic)
# -----------------------------
def create_face(mouth_open=0):
    """
    mouth_open: a float between 0 and 1 representing how wide the mouth is.
    """
    img = Image.new("RGB", (400, 400), "white")
    draw = ImageDraw.Draw(img)

    # Head Outline
    draw.ellipse((50, 80, 350, 350), outline="black", width=5)
    # Inner Face
    draw.ellipse((90, 120, 310, 320), outline="black", width=3)
    # Eyes
    draw.ellipse((140, 170, 180, 210), fill="black")
    draw.ellipse((220, 170, 260, 210), fill="black")

    # --- MOUTH ANIMATION ---
    # mouth_open 0 = closed line; 1 = wide open
    base_y = 260
    mouth_width_offset = 30
    
    # Calculate the vertical stretch of the lips
    lip_height = mouth_open * 40 
    
    # Draw the mouth (as an ellipse that expands downwards)
    draw.ellipse(
        (200 - mouth_width_offset, base_y, 200 + mouth_width_offset, base_y + lip_height), 
        outline="black", 
        width=4
    )

    # Antenna and Ears
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
# UI LAYOUT
# -----------------------------
left, right = st.columns([3, 1])

with right:
    st.markdown("## 🌐 GlobalInternet.py")
    st.markdown("**Owner:** Gesner Deslandes")
    st.markdown("📱 (509)-47385663")
    st.info("AI & Software Solutions 🇭🇹")

with left:
    st.title("🤖 Gesner Humanoid AI")
    language = st.selectbox("🌍 Select Language", list(voices.keys()))
    
    # Placeholder for the face
    frame = st.empty()
    frame.image(create_face(0))

    if st.button("▶️ Start Talking"):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
            audio_path = tmp.name

        with st.spinner("Preparing Voice..."):
            thread = threading.Thread(
                target=generate_voice_thread,
                args=(texts[language], voices[language], audio_path)
            )
            thread.start()
            thread.join()

        # Play Audio via HTML
        with open(audio_path, "rb") as f:
            audio_bytes = f.read()
        audio_base64 = base64.b64encode(audio_bytes).decode()
        
        st.markdown(
            f'<audio autoplay><source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3"></audio>',
            unsafe_allow_html=True
        )

        # Get MP3 length for the loop
        audio_info = MP3(audio_path)
        duration = audio_info.info.length

        # --- ANIMATION LOOP ---
        start_time = time.time()
        while time.time() - start_time < duration:
            elapsed = time.time() - start_time
            
            # Create a rhythmic "up and down" motion using absolute sine wave
            # Multiplying by 15 controls the speed of the lip movement
            mouth_val = abs(math.sin(elapsed * 15)) 
            
            frame.image(create_face(mouth_val))
            time.sleep(0.05) # ~20 frames per second for smoothness

        # Reset to closed mouth
        frame.image(create_face(0))
        
        # Cleanup
        if os.path.exists(audio_path):
            os.remove(audio_path)
