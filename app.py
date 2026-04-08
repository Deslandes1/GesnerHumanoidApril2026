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
# TEXTS
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
# FACE DESIGN (Talking Lips)
# -----------------------------
def create_face(mouth_open=0.0):
    img = Image.new("RGB", (400, 400), "white")
    draw = ImageDraw.Draw(img)

    # Face Shape
    draw.ellipse((50, 80, 350, 350), outline="black", width=5)
    draw.ellipse((90, 120, 310, 320), outline="black", width=3)
    
    # Eyes
    draw.ellipse((140, 170, 180, 210), fill="black")
    draw.ellipse((220, 170, 260, 210), fill="black")

    # --- UPDATED MOUTH LOGIC ---
    # We ensure the mouth has a clear "open" and "closed" state
    mouth_base_y = 245
    # Max height for the mouth opening
    max_open = 60 
    current_height = 5 + (mouth_open * max_open)
    
    # Drawing the "talking lips"
    draw.ellipse((165, mouth_base_y, 235, mouth_base_y + current_height), outline="black", width=5)

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
    st.markdown("**Owner:** Gesner Deslandes")
    st.markdown("📱 (509)-47385663")
    st.markdown("📧 deslandes78@gmail.com")
    st.markdown("🔗 [Main Website](https://globalinternetsitepy-abh7v6tnmskxxnuplrdcgk.streamlit.app/)")
    st.markdown("---")
    st.success("AI & Software Solutions 🇭🇹")

with left:
    st.title("🤖 Gesner Humanoid AI")
    st.markdown(
        "<div style='text-align:center;'><img src='https://upload.wikimedia.org/wikipedia/commons/5/56/Flag_of_Haiti.svg' width='120'></div>",
        unsafe_allow_html=True
    )

    language = st.selectbox("🌍 Select Language", list(voices.keys()))
    
    # This placeholder must exist before the loop
    frame = st.empty()
    frame.image(create_face(0.0))

    if st.button("▶️ Speak"):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
            audio_path = tmp.name

        with st.spinner("Preparing response..."):
            thread = threading.Thread(
                target=generate_voice_thread,
                args=(texts[language], voices[language], audio_path)
            )
            thread.start()
            thread.join()

        # Start Audio
        with open(audio_path, "rb") as f:
            audio_bytes = f.read()
        audio_base64 = base64.b64encode(audio_bytes).decode()
        
        st.markdown(
            f'<audio autoplay><source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3"></audio>',
            unsafe_allow_html=True
        )

        # Get Duration
        duration = MP3(audio_path).info.length

        # --- FORCED ANIMATION LOOP ---
        start_time = time.time()
        while time.time() - start_time < duration:
            elapsed = time.time() - start_time
            
            # Using a varied sine wave to make the mouth look like it's saying words
            # (Oscillates between 0.1 and 1.0)
            mouth_val = abs(math.sin(elapsed * 18)) * 0.8 + 0.1
            
            # Update the specific image placeholder
            frame.image(create_face(mouth_val))
            
            # Small sleep to allow Streamlit to render the new frame
            time.sleep(0.04)

        # Reset to neutral mouth after talking
        frame.image(create_face(0.0))

        # Cleanup
        if os.path.exists(audio_path):
            os.remove(audio_path)
