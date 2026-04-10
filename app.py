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
# VOICES & TEXTS (APRIL 2026 SCRIPT)
# -----------------------------
voices = {
    "English": "en-US-GuyNeural",
    "French": "fr-FR-HenriNeural",
    "Spanish": "es-ES-AlvaroNeural"
}

# The specific advertisement script
advert_script = """🌐 GlobalInternet.py est votre destination unique pour des logiciels Python sur mesure, construits d'Haïti vers le monde. 

👥 Notre équipe complète :
👨‍💼 Gesner Deslandes – Fondateur et PDG
👨‍💼 Gesner Junior Deslandes – Assistant du PDG
👨‍💻 Roosevelt Deslandes – Programmeur Python
👨‍💻 Sebastien Stephane Deslandes – Programmeur Python
👩‍💼 Zendaya Christelle Deslandes – Secrétaire

📅 Tous les nouveaux membres ont rejoint l’équipe en avril 2026. Bienvenue à bord.

⚙️ Nos services incluent :
🐍 Développement Python sur mesure
🧠 Solutions d’IA et de machine learning
🗳️ Systèmes complets de vote et d’élection
📊 Tableaux de bord décisionnels
🏫 Systèmes de gestion scolaire
📦 Gestion des stocks et point de vente
📈 Extraction de données web
♟️ Jeu d’échecs éducatif avec IA
🧮 Logiciel de comptabilité
📜 Base de données des archives nationales
🛡️ Radar de sécurité avancé DSM-2026

🎬 Des démos en direct sont disponibles pour la plupart des projets. 🔐 Accès démo protégé par mot de passe : 20082010

💰 Les prix varient de 20 USD à 2000 USD, licence unique.

📞 Contactez-nous pour vos besoins en logiciels sur mesure :
💬 WhatsApp : 509 4738-5663
📧 Email : deslandes78@gmail.com"""

# Clean version for TTS engine (removing emojis for better flow)
tts_clean_script = advert_script.replace("🌐", "").replace("👥", "").replace("👨‍💼", "").replace("👨‍💻", "").replace("👩‍💼", "").replace("📅", "").replace("⚙️", "").replace("🐍", "").replace("🧠", "").replace("🗳️", "").replace("📊", "").replace("🏫", "").replace("📦", "").replace("📈", "").replace("♟️", "").replace("🧮", "").replace("📜", "").replace("🛡️", "").replace("🎬", "").replace("🔐", "").replace("💰", "").replace("📞", "").replace("💬", "").replace("📧", "")

texts = {
    "English": tts_clean_script,
    "French": tts_clean_script,
    "Spanish": tts_clean_script
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
        draw.ellipse((140, center_y - 35, 260, center_y + 35), fill="black")
    else:
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
    st.markdown("**Founder & CEO:** Gesner Deslandes")
    st.markdown("📱 (509)-47385663")
    st.markdown("📧 deslandes78@gmail.com")
    st.markdown("🔗 [Main Website](https://globalinternetsitepy-abh7v6tnmskxxnuplrdcgk.streamlit.app/)")
    st.markdown("---")
    st.success("Haitian Software Mastery 🇭🇹")

with left:
    st.title("🤖 Gesner Humanoid AI")
    
    # THE HAITIAN FLAG
    st.markdown(
        "<div style='text-align:center;'><img src='https://upload.wikimedia.org/wikipedia/commons/5/56/Flag_of_Haiti.svg' width='120'></div>",
        unsafe_allow_html=True
    )
    
    language = st.selectbox("🌍 Select Language", list(voices.keys()), index=1)
    
    # TELEPROMPTER FOR VIEWERS
    st.markdown("### 📜 AI Teleprompter")
    st.text_area("Currently Reading:", value=advert_script, height=250)

    face_frame = st.empty()
    face_frame.image(create_face(is_open=False))

    if st.button("▶️ Launch GlobalInternet.py Advertisement"):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
            audio_path = tmp.name

        with st.spinner("AI preparing the company pitch..."):
            asyncio.run(edge_tts.Communicate(texts[language], voices[language]).save(audio_path))

        with open(audio_path, "rb") as f:
            b64 = base64.b64encode(f.read()).decode()
        
        duration = MP3(audio_path).info.length
        
        # Immediate audio start
        st.markdown(f'<audio autoplay><source src="data:audio/mp3;base64,{b64}" type="audio/mp3"></audio>', unsafe_allow_html=True)
        
        start_time = time.time()
        frame_toggle = True

        # THE AGGRESSIVE ANIMATION LOOP
        while (time.time() - start_time) < duration:
            face_frame.image(create_face(is_open=frame_toggle))
            frame_toggle = not frame_toggle
            time.sleep(0.04) 

        # Return to closed mouth
        face_frame.image(create_face(is_open=False))
        
        if os.path.exists(audio_path):
            os.remove(audio_path)
