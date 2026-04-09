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
# VOICES & TEXTS (CHESS TEACHING AI SCRIPT)
# -----------------------------
voices = {
    "English": "en-US-GuyNeural",
    "French": "fr-FR-HenriNeural",
    "Spanish": "es-ES-AlvaroNeural"
}

texts = {
    "English": """Learn Chess the Smart Way – with AI that teaches you! 
I'm proud to introduce Chess Teaching AI by my company GlobalInternet.py. 
This is an interactive chess app where you play against a powerful AI using Stockfish. 
It doesn't just beat you; it shows you the best move every turn. 
The app teaches you piece notation, winning strategies for all levels, and how to spot checkmates, forks, and pins. 
Learn the fastest mates like Scholar's Mate and solid openings like the Sicilian Dragon. 
Created by Gesner Deslandes, founder of GlobalInternet.py, building custom Python software from Haiti to the world. 
The best advice this app gives is: Before you move, ask yourself: what is my opponent threatening? 
Access the demo with password 20082010. Contact us on WhatsApp at 509-4738-5663. 
Stop memorizing moves – start understanding chess. Try it now!""",

    "French": """Apprenez les échecs de manière intelligente – avec une IA qui vous enseigne ! 
Je suis fier de présenter Chess Teaching AI par mon entreprise GlobalInternet.py. 
C'est une application d'échecs interactive où vous jouez contre une IA puissante utilisant Stockfish. 
Elle ne se contente pas de vous battre ; elle vous montre le meilleur coup à chaque tour. 
L'application vous enseigne la notation des pièces, des stratégies gagnantes pour tous les niveaux et comment repérer les échecs et mats, les fourchettes et les clouages. 
Apprenez les mats les plus rapides comme le coup du berger et des ouvertures solides comme la Dragon Sicilienne. 
Créé par Gesner Deslandes, fondateur de GlobalInternet.py, développant des logiciels Python personnalisés d'Haïti vers le monde. 
Le meilleur conseil de cette application est : Avant de bouger, demandez-vous : que menace mon adversaire ? 
Accédez à la démo avec le mot de passe 20082010. Contactez-nous sur WhatsApp au 509-4738-5663. 
Arrêtez de mémoriser les coups – commencez à comprendre les échecs. Essayez-le maintenant !""",

    "Spanish": """¡Aprende ajedrez de forma inteligente, con una IA que te enseña! 
Me enorgullece presentar Chess Teaching AI de mi empresa GlobalInternet.py. 
Esta es una aplicación de ajedrez interactiva donde juegas contra una potente IA que utiliza Stockfish. 
No solo te vence; te muestra el mejor movimiento en cada turno. 
La aplicación te enseña la notación de las piezas, estrategias ganadoras para todos los niveles y cómo detectar jaques mate, ataques dobles y clavadas. 
Aprende los mates más rápidos como el Mate del Pastor y aperturas sólidas como la Siciliana Dragón. 
Creado por Gesner Deslandes, fundador de GlobalInternet.py, construyendo software Python personalizado desde Haití para el mundo. 
El mejor consejo que da esta aplicación es: Antes de mover, pregúntate: ¿qué está amenazando mi oponente? 
Accede a la demo con la contraseña 20082010. Contáctanos por WhatsApp al 509-4738-5663. 
Deja de memorizar movimientos y empieza a entender el ajedrez. ¡Pruébalo ahora!"""
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
    st.markdown("🔗 [Main Website](https://globalinternetsitepy-abh7v6tnmskxxnuplrdcgk.streamlit.app/)")
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

    if st.button("▶️ Start Chess AI Announcement"):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
            audio_path = tmp.name

        with st.spinner("Gesner AI is starting the announcement..."):
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
