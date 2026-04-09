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
# VOICES & TEXTS
# -----------------------------
voices = {
    "English": "en-US-GuyNeural",
    "French": "fr-FR-HenriNeural",
    "Spanish": "es-ES-AlvaroNeural"
}

texts = {
    "English": """Master Chess with an AI that teaches you – not just plays against you. 
I'm Gesner Deslandes, founder of GlobalInternet.py, and I built this Chess Teaching AI to help you learn winning strategies while you play. 
What you learn: Why Nh3 means Knight to h3, piece symbols, and notation explained. 
Three winning moves for Beginner, Intermediate, and Advanced levels. 
How to spot checkmates, forks, pins, and discovered attacks. 
Fastest mates like Fool's Mate and Scholar's Mate, and solid openings like the Italian Game, Queen's Gambit, and Sicilian Dragon. 
Features include playing against Stockfish, world‑class AI. AI suggests the best move every turn. 
Choose any legal move from a dropdown and download your full move history. 
Available in four languages: English, Spanish, French, and Haitian Creole. 
Difficulty levels: Beginner, Intermediate, and Advanced. 
Demo access password is 20082010. Contact for custom software on WhatsApp at 509-4738-5663 or email deslandes78@gmail.com. 
GlobalInternet.py – Custom Python software from Haiti to the world. 
Full license is 149 dollars lifetime, includes all updates. 
Stop memorising – start understanding. Try the Chess Teaching AI today.""",

    "French": """Maîtrisez les échecs avec une IA qui vous enseigne, et pas seulement qui joue contre vous. 
Je suis Gesner Deslandes, fondateur de GlobalInternet.py, et j'ai créé cette IA d'enseignement des échecs pour vous aider à apprendre des stratégies gagnantes pendant que vous jouez. 
Ce que vous apprenez : Pourquoi Nh3 signifie Cavalier en h3, les symboles des pièces et la notation expliquée. 
Trois coups gagnants pour les niveaux débutant, intermédiaire et avancé. 
Comment repérer les échecs et mats, les fourchettes, les clouages et les attaques à la découverte. 
Les mats les plus rapides comme le coup du berger, et des ouvertures solides comme le Gambit de la Dame et la Dragon Sicilienne. 
Les fonctionnalités incluent le jeu contre Stockfish, une IA de classe mondiale. L'IA suggère le meilleur coup à chaque tour. 
Choisissez n'importe quel coup légal et téléchargez l'historique complet de vos coups. 
Disponible en quatre langues : anglais, espagnol, français et créole haïtien. 
Niveaux de difficulté : débutant, intermédiaire et avancé. 
Le mot de passe d'accès à la démo est 20082010. Contactez-nous pour un logiciel personnalisé sur WhatsApp au 509-4738-5663 ou par e-mail à deslandes78@gmail.com. 
GlobalInternet.py – Logiciels Python personnalisés d'Haïti vers le monde. 
La licence complète est de 149 dollars à vie, incluant toutes les mises à jour. 
Arrêtez de mémoriser, commencez à comprendre. Essayez l'IA d'enseignement des échecs dès aujourd'hui.""",

    "Spanish": """Domina el ajedrez con una IA que te enseña, no solo juega contra ti. 
Soy Gesner Deslandes, fundador de GlobalInternet.py, y creé esta IA de enseñanza de ajedrez para ayudarte a aprender estrategias ganadoras mientras juegas. 
Lo que aprendes: Por qué Nh3 significa Caballo a h3, los símbolos de las piezas y la notación explicada. 
Tres movimientos ganadores para los niveles principiante, intermedio y avanzado. 
Cómo detectar jaques mate, ataques dobles, clavadas y ataques descubiertos. 
Los mates más rápidos como el Mate del Pastor y aperturas sólidas como el Gambito de Dama y la Siciliana Dragón. 
Las características incluyen jugar contra Stockfish, IA de clase mundial. La IA sugiere el mejor movimiento en cada turno. 
Elige cualquier movimiento legal y descarga tu historial completo de movimientos. 
Disponible en cuatro idiomas: inglés, español, francés y criollo haitiano. 
Niveles de dificultad: principiante, intermedio y avanzado. 
La contraseña de acceso a la demo es 20082010. Contacte para software personalizado por WhatsApp al 509-4738-5663 o correo electrónico deslandes78@gmail.com. 
GlobalInternet.py – Software Python personalizado desde Haití para el mundo. 
La licencia completa cuesta 149 dólares de por vida, incluye todas las actualizaciones. 
Deja de memorizar, comienza a entender. Prueba la IA de enseñanza de ajedrez hoy mismo."""
}

# -----------------------------
# FACE DESIGN (AGGRESSIVE BLACK LIPS)
# -----------------------------
def create_face(is_open=False):
    img = Image.new("RGB", (400, 400), "white")
    draw = ImageDraw.Draw(img)

    # Face Shape
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

    if st.button("▶️ Start Aggressive Presentation"):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
            audio_path = tmp.name

        with st.spinner("Preparing Gesner Humanoid AI..."):
            asyncio.run(edge_tts.Communicate(texts[language], voices[language]).save(audio_path))

        # 1. LOAD AUDIO AS BASE64
        with open(audio_path, "rb") as f:
            b64 = base64.b64encode(f.read()).decode()
        
        # 2. GET DURATION BEFORE STARTING
        duration = MP3(audio_path).info.length
        
        # 3. START AUDIO & SYNC ANIMATION IMMEDIATELY
        st.markdown(f'<audio autoplay><source src="data:audio/mp3;base64,{b64}" type="audio/mp3"></audio>', unsafe_allow_html=True)
        
        start_time = time.time()
        frame_toggle = True

        # --- THE RELENTLESS ANIMATION LOOP ---
        while (time.time() - start_time) < duration:
            # Immediate flip for aggressive motion
            face_frame.image(create_face(is_open=frame_toggle))
            frame_toggle = not frame_toggle
            # 0.04s ensures we catch the eye and keeps up with speech tempo
            time.sleep(0.04) 

        # Final Close State
        face_frame.image(create_face(is_open=False))
        
        if os.path.exists(audio_path):
            os.remove(audio_path)
