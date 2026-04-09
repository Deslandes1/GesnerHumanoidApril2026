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
# VOICES & TEXTS (UPDATED FOR CHESS APP)
# -----------------------------
voices = {
    "English": "en-US-GuyNeural",
    "French": "fr-FR-HenriNeural",
    "Spanish": "es-ES-AlvaroNeural"
}

texts = {
    "English": """Welcome to GlobalInternet.py. Today, I am excited to present our Chess against the Machine application. 
This software allows you to challenge a powerful AI engine in a game of strategy and intellect. 
Whether you are a beginner or a grandmaster, our interface provides a smooth and professional experience. 
Visit us at global internet site p y to start playing now. 
For custom software, contact Gesner Deslandes at 509-47385663 or email deslandes78@gmail.com.""",

    "French": """Bienvenue chez GlobalInternet.py. Aujourd'hui, je suis ravi de vous présenter notre application d'échecs contre la machine. 
Ce logiciel vous permet de défier un moteur d'intelligence artificielle puissant dans un jeu de stratégie et d'intellect. 
Que vous soyez débutant ou grand maître, notre interface offre une expérience fluide et professionnelle. 
Visitez-nous sur global internet site p y pour commencer à jouer. 
Pour tout logiciel personnalisé, contactez Gesner Deslandes au 509-47385663 ou par email à deslandes78@gmail.com.""",

    "Spanish": """Bienvenido a GlobalInternet.py. Hoy, me complace presentar nuestra aplicación de Ajedrez contra la Máquina. 
Este software le permite desafiar a un potente motor de inteligencia artificial en un juego de estrategia e intelecto. 
Ya sea principiante o gran maestro, nuestra interfaz ofrece una experiencia fluida y profesional. 
Visítenos en global internet site p y para empezar a jugar. 
Para software personalizado, contacte a Gesner Deslandes al 509-47385663 o envíe un correo a deslandes78@gmail.com."""
}

# -----------------------------
# FACE DESIGN (AGGRESSIVE BLACK LIPS)
# -----------------------------
def create_face(is_open=False):
    img = Image.new("RGB", (400, 400), "white")
    draw = ImageDraw.Draw(img)

    # Face Outlines
    draw.ellipse((50, 80, 350, 350), outline="black", width=5)
    draw.ellipse((90, 120, 310, 320), outline="black", width=3)
    
    # Eyes
    draw.ellipse((140, 170, 180, 210), fill="black")
    draw.ellipse((220, 170, 260, 210), fill="black")

    # --- AGGRESSIVE BLACK MOUTH ---
    center_y = 265
    if is_open:
        # Huge black opening
        draw.ellipse((140, center_y - 35, 260, center_y + 35), fill="black")
    else:
        # Thick closed black line
        draw.line((150, center_y, 250, center_y), fill="black", width=12)

    # Robot Details
    draw.line((200, 80, 200, 40), fill="black", width=4)
    draw.ellipse((185, 20, 215, 50), outline="black", width=3)
    draw.rectangle((40, 180, 70, 260), outline="black", width=3)
    draw.rectangle((330, 180, 360, 260), outline="black", width=3)

    return img

# -----------------------------
# LOGIC & UI
# -----------------------------
left, right = st.columns([3, 1])

with right:
    st.markdown("## 🌐 GlobalInternet.py")
    st.markdown("**Owner:** Gesner Deslandes")
    st.markdown("📱 (509)-47385663")
    st.markdown("📧 deslandes78@gmail.com")
    st.markdown("🔗 [Click for Website](https://globalinternetsitepy-abh7v6tnmskxxnuplrdcgk.streamlit.app/)")
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
    
    face_frame = st.empty()
    face_frame.image(create_face(is_open=False))

    if st.button("▶️ Explain Chess App"):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
            audio_path = tmp.name

        with st.spinner("Gesner AI is starting..."):
            asyncio.run(edge_tts.Communicate(texts[language], voices[language]).save(audio_path))

        # Play Audio
        with open(audio_path, "rb") as f:
            b64 = base64.b64encode(f.read()).decode()
            st.markdown(f'<audio autoplay><source src="data:audio/mp3;base64,{b64}" type="audio/mp3"></audio>', unsafe_allow_html=True)

        # Precise Duration
        duration = MP3(audio_path).info.length
        start_time = time.time()

        # --- THE RELENTLESS ANIMATION LOOP ---
        frame_toggle = True
        while (time.time() - start_time) < duration:
            face_frame.image(create_face(is_open=frame_toggle))
            frame_toggle = not frame_toggle
            time.sleep(0.04) 

        # Final Close
        face_frame.image(create_face(is_open=False))
        
        if os.path.exists(audio_path):
            os.remove(audio_path)
