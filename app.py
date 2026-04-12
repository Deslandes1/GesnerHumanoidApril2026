import streamlit as st
from PIL import Image, ImageDraw
import asyncio
import edge_tts
import time
from mutagen.mp3 import MP3
import base64
import os
import tempfile
import requests
from io import BytesIO

st.set_page_config(layout="wide", page_title="Gesner Humanoid AI")

# ------------------------------
# HAITIAN FLAG
# ------------------------------
def show_haitian_flag(width=100):
    st.image("https://flagcdn.com/w320/ht.png", width=width)

# ------------------------------
# VOICES & PROMOTIONAL SCRIPT (New)
# ------------------------------
voices = {
    "English": "en-US-GuyNeural",
    "French": "fr-FR-HenriNeural"
}

promo_script_en = """
Attention! This is Gesner Humanoid AI with an exciting announcement!

GlobalInternet.py has just released three powerful new software solutions inspired by Silicon Valley engineering.

First: the *Task Manager Dashboard*. Inspired by React, this app lets you manage tasks, track progress, and analyze productivity with real‑time charts and dark mode. Perfect for teams and individuals.

Second: the *Ray Parallel Text Processor*. Inspired by UC Berkeley's distributed computing framework, this app shows you how to process text in parallel across multiple CPU cores. Watch the speedup – it’s up to 10x faster than sequential processing.

Third: the *Cassandra Data Dashboard*. Modeled after Apache Cassandra, the database that powers Netflix and Instagram, this app demonstrates a leaderless, wide‑column store for massive scalability. Add orders, search by customer, and explore real analytics.

All three apps include multi‑language support, password protection, and one‑time pricing. Each is fully customizable and ready to deploy.

Visit our main website to see live demos and purchase your license. Contact us for enterprise deals and custom development.

This is Gesner Humanoid AI for GlobalInternet.py. Build with Python. Deliver with speed. Innovate with AI. Thank you!
"""

promo_script_fr = """
Attention ! Ici l'IA Humanoïde Gesner pour une annonce passionnante !

GlobalInternet.py vient de lancer trois nouvelles solutions logicielles puissantes, inspirées par l'ingénierie de la Silicon Valley.

Premièrement : le *Tableau de bord des tâches*. Inspiré par React, cette application vous permet de gérer vos tâches, suivre votre progression et analyser votre productivité avec des graphiques en temps réel et un mode sombre. Parfait pour les équipes et les particuliers.

Deuxièmement : le *Processeur de texte parallèle Ray*. Inspiré par le framework de calcul distribué de UC Berkeley, cette application vous montre comment traiter du texte en parallèle sur plusieurs cœurs CPU. Regardez l’accélération – jusqu’à 10 fois plus rapide que le traitement séquentiel.

Troisièmement : le *Tableau de bord Cassandra*. Modélisé d’après Apache Cassandra, la base de données qui alimente Netflix et Instagram, cette application démontre un stockage sans leader, à colonnes larges, pour une scalabilité massive. Ajoutez des commandes, recherchez par client et explorez des analyses en temps réel.

Ces trois applications incluent le support multilingue, une protection par mot de passe et un prix unique. Chacune est entièrement personnalisable et prête à être déployée.

Visitez notre site principal pour voir les démos en direct et acheter votre licence. Contactez‑nous pour des offres entreprises et du développement sur mesure.

C'était l'IA Humanoïde Gesner pour GlobalInternet.py. Construisez avec Python. Livrez rapidement. Innovez avec l'IA. Merci !
"""

texts = {
    "English": promo_script_en,
    "French": promo_script_fr
}

# ------------------------------
# FACE DESIGN (AGGRESSIVE MOUTH)
# ------------------------------
def create_face(is_open=False):
    img = Image.new("RGB", (400, 400), "white")
    draw = ImageDraw.Draw(img)
    draw.ellipse((50, 80, 350, 350), outline="black", width=5)
    draw.ellipse((90, 120, 310, 320), outline="black", width=3)
    draw.ellipse((140, 170, 180, 210), fill="black")
    draw.ellipse((220, 170, 260, 210), fill="black")
    center_y = 265
    if is_open:
        draw.ellipse((110, center_y - 50, 290, center_y + 50), fill="black")
    else:
        draw.line((140, center_y, 260, center_y), fill="black", width=20)
    draw.line((200, 40, 200, 80), fill="black", width=4)
    draw.ellipse((185, 20, 215, 50), outline="black", width=3)
    return img

# ------------------------------
# UI LAYOUT
# ------------------------------
left, right = st.columns([3, 1])

with right:
    show_haitian_flag()
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
    st.subheader("🔥 New Software Releases – Silicon Valley Inspired")
    
    language = st.selectbox("🌍 Select Language", list(voices.keys()))
    
    face_placeholder = st.empty()
    face_placeholder.image(create_face(is_open=False))
    audio_placeholder = st.empty()

    if st.button("🚀 Play Promotional Announcement"):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
            audio_path = tmp.name
        with st.spinner("Generating audio..."):
            asyncio.run(edge_tts.Communicate(texts[language], voices[language]).save(audio_path))
        with open(audio_path, "rb") as f:
            audio_bytes = f.read()
            b64 = base64.b64encode(audio_bytes).decode()
        duration = MP3(audio_path).info.length
        audio_html = f"""
            <audio autoplay="true" controls style="width: 100%;">
                <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
            </audio>
        """
        audio_placeholder.markdown(audio_html, unsafe_allow_html=True)
        start_time = time.time()
        toggle = True
        while (time.time() - start_time) < duration:
            face_placeholder.image(create_face(is_open=toggle))
            toggle = not toggle
            time.sleep(0.04)
        face_placeholder.image(create_face(is_open=False))
        if os.path.exists(audio_path):
            os.remove(audio_path)

st.markdown("---")
st.markdown("🇭🇹 *Gesner Humanoid AI – Promoting GlobalInternet.py software excellence.* 🇭🇹")
