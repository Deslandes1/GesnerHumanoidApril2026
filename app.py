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
# FACE DESIGN (HIGH-VISIBILITY MOUTH)
# -----------------------------
def create_face(mouth_val=0.0):
    img = Image.new("RGB", (400, 400), "white")
    draw = ImageDraw.Draw(img)

    # Face Shape
    draw.ellipse((50, 80, 350, 350), outline="black", width=5)
    draw.ellipse((90, 120, 310, 320), outline="black", width=3)
    
    # Eyes
    draw.ellipse((140, 170, 180, 210), fill="black")
    draw.ellipse((220, 170, 260, 210), fill="black")

    # --- THE MOUTH (ANCHORED & DYNAMIC) ---
    center_y = 260
    # Make the opening very visible (up to 40 pixels)
    opening = 2 + (mouth_val * 40)
    
    y0 = center_y - (opening / 2)
    y1 = center_y + (opening / 2)
    
    # Red lips to make the motion even more obvious
    draw.ellipse((150, y0, 250, y1), outline="red", width=6)

    # Decoration
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
# LAYOUT
# -----------------------------
left, right = st.columns([3, 1])

with right:
    st.markdown("## 🌐 GlobalInternet.py")
    st.markdown("**Owner:** Gesner Deslandes")
    st.markdown("📱 (509)-47385663")
    st.markdown("📧 deslandes78@gmail.com")
    st.markdown("🔗 [Click for Site](https://globalinternetsitepy-abh7v6tnmskxxnuplrdcgk.streamlit.app/)")
    st.markdown("---")
    st.success("AI & Software Solutions 🇭🇹")

with left:
    st.title("🤖 Gesner Humanoid AI")
    
    # THE HAITIAN FLAG
    st.markdown(
        "<div style='text-align:center;'><img src='https://upload.wikimedia.org/wikipedia/commons/5/56/Flag_of_Haiti.svg' width='120'></div>",
        unsafe_allow_html=True
    )
    
    language = st.selectbox("🌍 Select Language", list(voices.keys()))
    
    # Placeholder for the face
    face_frame = st.empty()
    face_frame.image(create_face(0.0))

    if st.button("▶️ Start Speaking"):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
            audio_path = tmp.name

        with st.spinner("Generating audio..."):
            asyncio.run(generate_voice(texts[language], voices[language], audio_path))

        # Start Audio via HTML
        with open(audio_path, "rb") as f:
            b64 = base64.b64encode(f.read()).decode()
            st.markdown(f'<audio autoplay><source src="data:audio/mp3;base64,{b64}" type="audio/mp3"></audio>', unsafe_allow_html=True)

        # Get total duration
        duration = MP3(audio_path).info.length
        start_time = time.time()

        # --- THE FINAL ANIMATION LOOP ---
        # We use a while loop that checks the clock against the audio duration
        while True:
            elapsed = time.time() - start_time
            if elapsed >= duration:
                break
            
            # Rapid sine wave for speech effect
            mouth_movement = abs(math.sin(elapsed * 22))
            
            # Force the update
            face_frame.image(create_face(mouth_movement))
            
            # Small delay to keep the CPU stable but the animation fast
            time.sleep(0.03)

        # Ensure mouth is closed at the exact end
        face_frame.image(create_face(0.0))
        
        # Cleanup
        if os.path.exists(audio_path):
            os.remove(audio_path)
