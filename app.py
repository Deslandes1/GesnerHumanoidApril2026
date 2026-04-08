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
# FACE DESIGN (BLACK LIPS - STABLE)
# -----------------------------
def create_face(mouth_open=False):
    img = Image.new("RGB", (400, 400), "white")
    draw = ImageDraw.Draw(img)

    # Face Shape
    draw.ellipse((50, 80, 350, 350), outline="black", width=5)
    draw.ellipse((90, 120, 310, 320), outline="black", width=3)
    
    # Eyes
    draw.ellipse((140, 170, 180, 210), fill="black")
    draw.ellipse((220, 170, 260, 210), fill="black")

    # --- THE MOUTH (BLACK COLOR) ---
    center_y = 260
    
    if mouth_open:
        # Open state: A clear black oval
        draw.ellipse((150, center_y - 25, 250, center_y + 25), outline="black", width=8)
    else:
        # Closed state: A flat black line
        draw.line((160, center_y, 240, center_y), fill="black", width=6)

    # Robot details
    draw.line((200, 80, 200, 40), fill="black", width=4)
    draw.ellipse((185, 20, 215, 50), outline="black", width=3)
    draw.rectangle((40, 180, 70, 260), outline="black", width=3)
    draw.rectangle((330, 180, 360, 260), outline="black", width=3)

    return img

# -----------------------------
# VOICE GENERATOR
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
    
    # HAITIAN FLAG RESTORED
    st.markdown(
        "<div style='text-align:center;'><img src='https://upload.wikimedia.org/wikipedia/commons/5/56/Flag_of_Haiti.svg' width='120'></div>",
        unsafe_allow_html=True
    )
    
    language = st.selectbox("🌍 Select Language", list(voices.keys()))
    
    face_frame = st.empty()
    face_frame.image(create_face(mouth_open=False))

    if st.button("▶️ Start Speaking"):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
            audio_path = tmp.name

        with st.spinner("Preparing speech..."):
            asyncio.run(generate_voice(texts[language], voices[language], audio_path))

        # Start Audio via HTML
        with open(audio_path, "rb") as f:
            b64 = base64.b64encode(f.read()).decode()
            st.markdown(f'<audio autoplay><source src="data:audio/mp3;base64,{b64}" type="audio/mp3"></audio>', unsafe_allow_html=True)

        # Get Duration
        duration = MP3(audio_path).info.length
        start_time = time.time()

        # --- ANIMATION LOOP ---
        counter = 0
        while (time.time() - start_time) < duration:
            # Alternates the mouth state every few frames for a flickering "talk" effect
            is_open = (counter % 4 < 2) 
            
            face_frame.image(create_face(mouth_open=is_open))
            
            counter += 1
            time.sleep(0.06)

        # Ensure mouth is closed at the end
        face_frame.image(create_face(mouth_open=False))
        
        # Cleanup
        if os.path.exists(audio_path):
            os.remove(audio_path)
