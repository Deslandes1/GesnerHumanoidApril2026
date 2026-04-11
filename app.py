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
# VOICES & AI IMAGE CLASSIFIER SCRIPT
# -----------------------------
voices = {
    "English": "en-US-GuyNeural",
    "French": "fr-FR-HenriNeural"
}

# The specific script for the AI Image Classifier presentation
classifier_script_en = """
Hello everyone! Today I am presenting the AI Image Classifier app, built by GlobalInternet.py. 
This app uses a pre-trained neural network called MobileNetV2 that recognizes one thousand everyday objects, animals, vehicles, and common items.
For the best results, you should upload clear images of animals, vehicles, food, electronics, household items, or nature scenes. 
Please note, do not upload personal family photos, text documents, or medical images, as this model is a proof-of-concept for object recognition.
This high-quality AI Classifier software is available for one thousand two hundred dollars. This includes a one-time license, the full source code, setup, and one year of support.
GlobalInternet.py provides Python software and AI solutions from Haiti to the world. 
Thank you to Mister Gesner Deslandes for leading this innovation!
"""

classifier_script_fr = """
Bonjour à tous ! Aujourd'hui, je vous présente l'application AI Image Classifier, conçue par GlobalInternet.py.
Cette application utilise un réseau de neurones pré-entraîné appelé MobileNetV2 qui reconnaît mille objets du quotidien, animaux, véhicules et articles courants.
Pour obtenir les meilleurs résultats, vous devez télécharger des images claires d'animaux, de véhicules, de nourriture, d'électronique ou de scènes de nature.
Veuillez noter : ne téléchargez pas de photos de famille personnelles ou de documents médicaux, car ce modèle est une preuve de concept pour la reconnaissance d'objets.
Ce logiciel de classification par IA est disponible pour mille deux cents dollars. Cela comprend une licence unique, le code source complet, la configuration et un an de support.
GlobalInternet.py fournit des logiciels Python et des solutions d'IA d'Haïti au reste du monde.
Merci à Monsieur Gesner Deslandes pour avoir dirigé cette innovation !
"""

texts = {
    "English": classifier_script_en,
    "French": classifier_script_fr
}

# -----------------------------
# FACE DESIGN
# -----------------------------
def create_face(is_open=False):
    img = Image.new("RGB", (400, 400), "white")
    draw = ImageDraw.Draw(img)
    # Face Structure
    draw.ellipse((50, 80, 350, 350), outline="black", width=5)
    draw.ellipse((90, 120, 310, 320), outline="black", width=3)
    # Eyes
    draw.ellipse((140, 170, 180, 210), fill="black")
    draw.ellipse((220, 170, 260, 210), fill="black")
    # Mouth Animation Logic
    center_y = 265
    if is_open:
        draw.ellipse((140, center_y - 30, 260, center_y + 30), fill="black")
    else:
        draw.line((150, center_y, 250, center_y), fill="black", width=12)
    # Antenna
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
    st.markdown("📱 (509) 4738-5663")
    st.markdown("📧 deslandes78@gmail.com")
    st.markdown("🔗 [Portfolio](https://globalinternetsitepy-abh7v6tnmskxxnuplrdcgk.streamlit.app/)")
    st.success("Python Specialist 🐍")

with left:
    st.title("🤖 Gesner Humanoid AI")
    st.subheader("App Showcase: AI Image Classifier")
    
    st.markdown("<div style='text-align:center;'><img src='https://upload.wikimedia.org/wikipedia/commons/5/56/Flag_of_Haiti.svg' width='100'></div>", unsafe_allow_html=True)
    
    language = st.selectbox("🌍 Select Language", list(voices.keys()))
    
    face_placeholder = st.empty()
    face_placeholder.image(create_face(is_open=False))

    if st.button("▶️ Start AI Presentation"):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
            audio_path = tmp.name
        
        with st.spinner("Analyzing Script..."):
            asyncio.run(edge_tts.Communicate(texts[language], voices[language]).save(audio_path))
        
        with open(audio_path, "rb") as f:
            b64 = base64.b64encode(f.read()).decode()
        
        duration = MP3(audio_path).info.length
        st.markdown(f'<audio autoplay><source src="data:audio/mp3;base64,{b64}" type="audio/mp3"></audio>', unsafe_allow_html=True)
        
        # SYNCED MOUTH ANIMATION
        start_time = time.time()
        toggle = True
        while (time.time() - start_time) < duration:
            face_placeholder.image(create_face(is_open=toggle))
            toggle = not toggle
            time.sleep(0.05)
        
        face_placeholder.image(create_face(is_open=False))
        if os.path.exists(audio_path):
            os.remove(audio_path)
