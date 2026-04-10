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
# VOICES & SELF-INTRODUCTION SCRIPTS
# -----------------------------
voices = {
    "English": "en-US-GuyNeural",
    "French": "fr-FR-HenriNeural",
    "Spanish": "es-ES-AlvaroNeural"
}

# The new social media introduction script
intro_en = """Hello to everyone on social media! I am the Gesner Humanoid AI, a digital representative of innovation. I was built by Gesner Deslandes, a professional Python builder and the founder of GlobalInternet.py. I am a manifestation of software expertise, designed to bridge the gap between human interaction and advanced technology. Whether it is through code, creativity, or connectivity, we are here to provide fast software solutions to the world. To conclude, I want to say a huge thank you to Mister Gesner Deslandes of GlobalInternet.py for bringing me to life. Thank you!"""

intro_fr = """Bonjour à tous sur les réseaux sociaux ! Je suis l'IA Humanoïde Gesner, une représentation numérique de l'innovation. J'ai été conçu par Gesner Deslandes, un développeur Python et le fondateur de GlobalInternet.py. Je suis la manifestation d'une expertise logicielle, créée pour combler le fossé entre l'interaction humaine et la technologie avancée. Que ce soit par le code, la créativité ou la connectivité, nous sommes ici pour fournir des solutions logicielles rapides au monde entier. Pour conclure, je tiens à dire un grand merci à Monsieur Gesner Deslandes de GlobalInternet.py pour m'avoir donné vie. Merci !"""

texts = {
    "English": intro_en,
    "French": intro_fr,
    "Spanish": """Hola a todos en las redes sociales. Soy la IA Humanoide de Gesner, construida por Gesner Deslandes de GlobalInternet.py. Gracias a Mister Gesner Deslandes de GlobalInternet.py por darme vida."""
}

# -----------------------------
# FACE DESIGN
# -----------------------------
def create_face(is_open=False):
    img = Image.new("RGB", (400, 400), "white")
    draw = ImageDraw.Draw(img)
    draw.ellipse((50, 80, 350, 350), outline="black", width=5)
    draw.ellipse((90, 120, 310, 320), outline="black", width=3)
    draw.ellipse((140, 170, 180, 210), fill="black")
    draw.ellipse((220, 170, 260, 210), fill="black")
    center_y = 265
    if is_open:
        draw.ellipse((140, center_y - 30, 260, center_y + 30), fill="black")
    else:
        draw.line((150, center_y, 250, center_y), fill="black", width=12)
    draw.line((200, 40, 200, 80), fill="black", width=4)
    draw.ellipse((185, 20, 215, 50), outline="black", width=3)
    return img

# -----------------------------
# UI LAYOUT
# -----------------------------
left, right = st.columns([3, 1])

with right:
    # PROFESSIONAL COMPANY BRANDING
    st.markdown("""
        <div style="background-color: #003366; padding: 20px; border-radius: 10px; text-align: center;">
            <h2 style="color: white; margin: 0;">GlobalInternet.py</h2>
            <p style="color: #66ccff; font-size: 0.9em;">Fast Software Solutions</p>
        </div>
    """, unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("**Builder & Founder:**")
    st.markdown("### Gesner Deslandes")
    st.markdown("📱 (509)-47385663")
    st.markdown("📧 deslandes78@gmail.com")
    st.markdown("🔗 [Portfolio](https://globalinternetsitepy-abh7v6tnmskxxnuplrdcgk.streamlit.app/)")
    st.success("Python Specialist 🐍")

with left:
    st.title("🤖 Gesner Humanoid AI")
    st.markdown("<div style='text-align:center;'><img src='https://upload.wikimedia.org/wikipedia/commons/5/56/Flag_of_Haiti.svg' width='100'></div>", unsafe_allow_html=True)
    
    language = st.selectbox("🌍 Select Language", list(voices.keys()))
    
    face_placeholder = st.empty()
    face_placeholder.image(create_face(is_open=False))

    if st.button("▶️ Start Introduction"):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
            audio_path = tmp.name
        
        with st.spinner("Initializing AI Persona..."):
            asyncio.run(edge_tts.Communicate(texts[language], voices[language]).save(audio_path))
        
        with open(audio_path, "rb") as f:
            b64 = base64.b64encode(f.read()).decode()
        
        duration = MP3(audio_path).info.length
        st.markdown(f'<audio autoplay><source src="data:audio/mp3;base64,{b64}" type="audio/mp3"></audio>', unsafe_allow_html=True)
        
        start_time = time.time()
        toggle = True
        while (time.time() - start_time) < duration:
            face_placeholder.image(create_face(is_open=toggle))
            toggle = not toggle
            time.sleep(0.05)
        
        face_placeholder.image(create_face(is_open=False))
        if os.path.exists(audio_path):
            os.remove(audio_path)
