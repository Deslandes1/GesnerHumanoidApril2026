import streamlit as st
from PIL import Image, ImageDraw
import asyncio
import edge_tts
import time
import os
import base64

st.set_page_config(page_title="Gesner Humanoid AI", layout="wide")

# -----------------------------
# VOICE SETTINGS
# -----------------------------
voices = {
    "English": "en-US-GuyNeural",
    "French": "fr-FR-HenriNeural",
    "Spanish": "es-ES-AlvaroNeural"
}

# -----------------------------
# FULL SPEECH PER LANGUAGE
# -----------------------------
texts = {
    "English": """Accountant Excel Advanced AI April 2026.

This is Gesner Deslandes, founder of GlobalInternet.py.

A complete accounting and loan tracking system that replaces messy spreadsheets.

Manage cash flow, track loans, and generate professional reports all in one secure web app.

You can record cash in and cash out, track your real-time balance, and manage loans with automatic calculations.

Add borrowers, define payment schedules, track payments, and view full history.

Generate professional reports including cash flow, loan status, and payment history.

Export everything to Excel and PDF.

The system is multilingual and secure with login and logout functionality.

Perfect for businesses, NGOs, schools, and government offices.

One-time payment: one hundred forty-nine US dollars with lifetime access.

Send payment via Moncash and receive access within twenty-four hours.

Built in Haiti by GlobalInternet.py for the world.

Order today and simplify your accounting tomorrow.""",

    "French": """Accountant Excel Advanced AI avril 2026.

Je suis Gesner Deslandes, fondateur de GlobalInternet.py.

Un système complet de comptabilité et de gestion de prêts qui remplace Excel.

Gérez les entrées et sorties d’argent, suivez le solde en temps réel et les prêts automatiquement.

Ajoutez des emprunteurs, définissez les paiements et suivez l’historique complet.

Générez des rapports professionnels exportables en Excel et PDF.

Application sécurisée, multilingue avec connexion et déconnexion.

Idéal pour entreprises, ONG, écoles et institutions.

Paiement unique de 149 dollars avec accès à vie.

Fabriqué en Haïti pour le monde.

Commandez aujourd’hui et simplifiez votre comptabilité.""",

    "Spanish": """Accountant Excel Advanced AI abril 2026.

Soy Gesner Deslandes, fundador de GlobalInternet.py.

Un sistema completo de contabilidad y gestión de préstamos que reemplaza Excel.

Registra ingresos y gastos, controla el balance en tiempo real y gestiona préstamos automáticamente.

Agrega clientes, define pagos y revisa el historial completo.

Genera reportes profesionales exportables en Excel y PDF.

Sistema seguro y multilingüe.

Ideal para empresas, ONG, escuelas y gobiernos.

Pago único de 149 dólares con acceso de por vida.

Hecho en Haití para el mundo.

Ordena hoy y simplifica tu contabilidad."""
}

# -----------------------------
# CREATE ROBOT FACE
# -----------------------------
def create_face(mouth_open=False):
    img = Image.new("RGB", (400, 400), "white")
    draw = ImageDraw.Draw(img)

    # Head
    draw.ellipse((50, 80, 350, 350), outline="black", width=5)

    # Inner face
    draw.ellipse((90, 120, 310, 320), outline="black", width=4)

    # Eyes
    draw.ellipse((140, 170, 180, 210), fill="black")
    draw.ellipse((220, 170, 260, 210), fill="black")

    # Mouth animation
    if mouth_open:
        draw.ellipse((170, 240, 230, 300), outline="black", width=4)
    else:
        draw.arc((150, 230, 250, 300), start=0, end=180, fill="black", width=4)

    # Antenna
    draw.line((200, 80, 200, 40), fill="black", width=4)
    draw.ellipse((185, 20, 215, 50), outline="black", width=3)

    # Side panels
    draw.rectangle((40, 180, 70, 260), outline="black", width=3)
    draw.rectangle((330, 180, 360, 260), outline="black", width=3)

    return img

# -----------------------------
# GENERATE VOICE
# -----------------------------
async def generate_voice(text, voice):
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save("voice.mp3")

# -----------------------------
# ESTIMATE SPEECH DURATION
# -----------------------------
def estimate_duration(text):
    words = len(text.split())
    return words / 2.5

# -----------------------------
# STREAMLIT UI WITH HAITIAN FLAG ON THE LEFT
# -----------------------------
# Create three columns: flag, content, empty spacer
col_flag, col_main, col_right = st.columns([1, 3, 1])

with col_flag:
    st.image("https://flagcdn.com/w320/ht.png", width=120)

with col_main:
    st.title("🤖 Gesner Humanoid AI")
    language = st.selectbox("🌍 Select Language", list(voices.keys()))
    frame = st.empty()
    frame.image(create_face(False))

    if st.button("▶️ Speak"):
        # Generate voice
        asyncio.run(generate_voice(texts[language], voices[language]))

        # Play audio
        audio_file = open("voice.mp3", "rb")
        st.audio(audio_file.read(), format="audio/mp3")

        # Animate mouth based on speech duration
        duration = estimate_duration(texts[language])
        start = time.time()
        while time.time() - start < duration:
            frame.image(create_face(True))
            time.sleep(0.2)
            frame.image(create_face(False))
            time.sleep(0.2)
        frame.image(create_face(False))

with col_right:
    st.markdown("""
    <div style='text-align: right;'>
        <b>GlobalInternet.py</b><br>
        Gesner Deslandes<br>
        Python Developer
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")
st.markdown("© 2026 GlobalInternet.py – All rights reserved")
