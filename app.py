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
# VOICES & TEXTS (LATEST CHESS SCRIPT)
# -----------------------------
voices = {
    "English": "en-US-GuyNeural",
    "French": "fr-FR-HenriNeural",
    "Spanish": "es-ES-AlvaroNeural"
}

# Unified script for the AI to read across all selected languages
texts = {
    "English": """Master Chess with an AI that teaches you – not just plays against you. 
I'm Gesner Deslandes, founder of GlobalInternet.py, and I built this Chess Teaching AI to help you learn winning strategies while you play. 
You will learn why Nh3 means Knight to h3, piece symbols, and notation. 
Discover three winning moves for Beginner, Intermediate, and Advanced levels. 
Learn how to spot checkmates, forks, pins, and discovered attacks. 
Master the fastest mates like Fool's Mate and Scholar's Mate, and solid openings like the Sicilian Dragon. 
Features include playing against Stockfish, AI move suggestions every turn, and downloading your full move history. 
The app is available in four languages: English, Spanish, French, and Haitian Creole. 
Demo access uses password 20082010. Contact us for custom software on WhatsApp at 509-4738-5663. 
The full license is 149 dollars. Stop memorizing – start understanding. Try the Chess Teaching AI today.""",

    "French": """Maîtrisez les échecs avec une IA qui vous enseigne, et pas seulement qui joue contre vous. 
Je suis Gesner Deslandes, fondateur de GlobalInternet.py, et j'ai créé cette IA d'enseignement des échecs pour vous aider à apprendre des stratégies gagnantes pendant que vous jouez. 
Vous apprendrez pourquoi Nh3 signifie Cavalier en h3, les symboles des pièces et la notation. 
Découvrez trois coups gagnants pour les niveaux débutant, intermédiaire et avancé. 
Apprenez à repérer les échecs et mats, les fourchettes, les clouages et les attaques à la découverte. 
Maîtrisez les mats les plus rapides comme le coup du berger, et des ouvertures solides comme la Dragon Sicilienne. 
Les fonctionnalités incluent le jeu contre Stockfish, des suggestions de coups par l'IA à chaque tour et le téléchargement de l'historique de vos coups. 
L'application est disponible en quatre langues : anglais, espagnol, français et créole haïtien. 
L'accès à la démo utilise le mot de passe 20082010. Contactez-nous pour un logiciel personnalisé sur WhatsApp au 509-4738-5663. 
La licence complète est de 149 dollars. Arrêtez de mémoriser, commencez à comprendre. Essayez l'IA d'enseignement des échecs dès aujourd'hui.""",

    "Spanish": """Domina el ajedrez con una IA que te enseña, no solo juega contra ti. 
Soy Gesner Deslandes, fundador de GlobalInternet.py, y creé esta IA de enseñanza de ajedrez para ayudarte a aprender estrategias ganadoras mientras juegas. 
Aprenderás por qué Nh3 significa Caballo a h3, los símbolos de las piezas y la notación. 
Descubre tres movimientos ganadores para los niveles principiante, intermedio y avanzado. 
Aprende a detectar jaques mate, ataques dobles, clavadas y ataques descubiertos. 
Domina los mates más rápidos como el Mate del Pastor y aperturas sólidas como la Siciliana Dragón. 
Las características incluyen jugar contra Stockfish, sugerencias de movimientos de IA en cada turno y la descarga de tu historial de movimientos. 
La aplicación está disponible en cuatro idiomas: inglés, español, francés y criollo haitiano. 
El acceso a la demo utiliza la contraseña 20082010. Contáctenos para software personalizado por WhatsApp al 509-4738-5663. 
La licencia completa cuesta 149 dólares. Deja de memorizar, comienza a entender. Prueba la IA de enseñanza de ajedrez hoy mismo."""
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

    if st.button("▶️ Play Master Chess Script"):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
            audio_path = tmp.name

        with st.spinner("Gesner AI is starting the masterclass..."):
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
