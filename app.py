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
# VOICES & PROMOTIONAL SCRIPT
# -----------------------------
voices = {
    "English": "en-US-GuyNeural",
    "French": "fr-FR-HenriNeural"
}

# High-energy promotional script
promo_script_en = """
Attention! This is Gesner Humanoid AI with a special announcement!
Are you looking for the fastest way to support your loved ones in Haiti? Look no further than Western Union! 
We know that family is everything. Whether it is for food, medicine, or school fees, your support needs to arrive safely and without delay!
Why choose Western Union? 
First! Speed! Your money is ready for pickup in just minutes. 
Second! Accessibility! With thousands of locations from Port-au-Prince to the smallest villages, we are everywhere you need us to be. 
Third! Security! Trust the leader with over one hundred and fifty years of experience!
And fourth! Simplicity! No bank account? No problem! Just a name and a pickup location is all it takes.
To every Haitian abroad: Your family is waiting! Don't let distance stand in the way. 
Send with confidence. Send with Western Union today! 
Visit your nearest agent or download the app now. 
This is Gesner Humanoid AI for GlobalInternet.py. Keep Haiti strong! Send now!
"""

promo_script_fr = """
Attention ! Ici l'IA Humanoïde Gesner pour une annonce spéciale !
Vous cherchez le moyen le plus rapide de soutenir vos proches en Haïti ? Ne cherchez plus, choisissez Western Union !
La famille est ce qu'il y a de plus important. Que ce soit pour la nourriture, les médicaments ou les frais scolaires, votre soutien doit arriver en toute sécurité et sans délai !
Pourquoi choisir Western Union ?
Premièrement ! La Rapidité ! Votre argent est prêt en quelques minutes seulement.
Deuxièmement ! L'Accessibilité ! Avec des milliers d'agences de Port-au-Prince aux plus petits villages, nous sommes partout où vous avez besoin de nous.
Troisièmement ! La Sécurité ! Faites confiance au leader avec plus de cent cinquante ans d'expérience !
Et quatrièmement ! La Simplicité ! Pas de compte bancaire ? Aucun problème ! Un nom et un lieu de retrait suffisent.
À tous les Haïtiens à l'étranger : Votre famille vous attend ! Ne laissez pas la distance vous arrêter.
Envoyez en toute confiance. Envoyez avec Western Union dès aujourd'hui !
Visitez votre agent le plus proche ou téléchargez l'application maintenant.
C'était l'IA Humanoïde Gesner pour GlobalInternet.py. Gardez Haïti forte ! Envoyez maintenant !
"""

texts = {
    "English": promo_script_en,
    "French": promo_script_fr
}

# -----------------------------
# FACE DESIGN (AGGRESSIVE MOUTH)
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
    
    # --- AGGRESSIVE MOUTH MOVEMENT ---
    center_y = 265
    if is_open:
        # Extra Large, aggressive open mouth
        draw.ellipse((110, center_y - 50, 290, center_y + 50), fill="black")
    else:
        # Very thick, heavy aggressive closed line
        draw.line((140, center_y, 260, center_y), fill="black", width=20)
        
    # Antenna
    draw.line((200, 40, 200, 80), fill="black", width=4)
    draw.ellipse((185, 20, 215, 50), outline="black", width=3)
    return img

# -----------------------------
# UI LAYOUT
# -----------------------------
left, right = st.columns([3, 1])

with right:
    # WESTERN UNION PROMO BRANDING
    st.markdown("""
        <div style="background-color: #FFCC00; padding: 15px; border-radius: 10px; text-align: center; border: 3px solid black;">
            <h1 style="color: black; margin: 0; font-family: 'Arial Black', sans-serif; letter-spacing: -1px;">WESTERN<br>UNION</h1>
            <p style="color: black; font-weight: bold; margin-top: 5px;">SEND NOW</p>
        </div>
    """, unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("""
        <div style="background-color: #003366; padding: 20px; border-radius: 10px; text-align: center;">
            <h2 style="color: white; margin: 0;">GlobalInternet.py</h2>
            <p style="color: #66ccff; font-size: 0.9em;">Innovation & Tech</p>
        </div>
    """, unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("**Builder & Founder:**")
    st.markdown("### Gesner Deslandes")
    st.markdown("📱 (509) 4738-5663")
    st.markdown("📧 deslandes78@gmail.com")
    st.markdown("🔗 [Main Platform](https://globalinternetsitepy-abh7v6tnmskxxnuplrdcgk.streamlit.app/)")
    st.success("Building the Future 🇭🇹")

with left:
    st.title("🤖 Gesner Humanoid AI")
    st.subheader("🔥 Special Promotion: Western Union x Haiti")
    
    language = st.selectbox("🌍 Select Language", list(voices.keys()))
    
    face_placeholder = st.empty()
    face_placeholder.image(create_face(is_open=False))
    
    audio_placeholder = st.empty()

    if st.button("🚀 Start Promotional Announcement"):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
            audio_path = tmp.name
        
        with st.spinner("Generating High-Energy Audio..."):
            asyncio.run(edge_tts.Communicate(texts[language], voices[language]).save(audio_path))
        
        with open(audio_path, "rb") as f:
            audio_bytes = f.read()
            b64 = base64.b64encode(audio_bytes).decode()
        
        duration = MP3(audio_path).info.length
        
        # Audio rendering with controls
        audio_html = f"""
            <audio autoplay="true" controls style="width: 100%;">
                <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
            </audio>
        """
        audio_placeholder.markdown(audio_html, unsafe_allow_html=True)
        
        # --- AGGRESSIVE ANIMATION ENGINE ---
        # Forces the mouth to stay in motion for the full duration
        start_time = time.time()
        toggle = True
        
        while (time.time() - start_time) < duration:
            face_placeholder.image(create_face(is_open=toggle))
            toggle = not toggle
            # High-speed toggle for intense promotional look
            time.sleep(0.04) 
        
        # Final reset to closed mouth
        face_placeholder.image(create_face(is_open=False))
        
        if os.path.exists(audio_path):
            os.remove(audio_path)
