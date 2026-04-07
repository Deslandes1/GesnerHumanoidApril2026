import streamlit as st
from PIL import Image, ImageDraw
import asyncio
import edge_tts
import time
import os

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
    "English": """Official Online Voting System for Haiti Elections.

Developed by GlobalInternet.py, owned by Gesner Deslandes.

We have created a complete, secure, and multilingual online voting platform built entirely in Python.

This system is designed for the Haitian government, the CEP, and any electoral institution to modernize elections with transparency and real-time results.

Key features include multilingual interface in Creole, French, English, and Spanish.

Each voter receives a unique ID to prevent double voting.

The CEP President has full control through a powerful dashboard to manage candidates.

Votes are tracked in real time, showing live results and current leaders.

Instant PDF reports can be generated for media and observers.

Candidate profiles include images, symbols, and slogans.

A neutral voting option is available.

Election duration is controlled with automatic closing.

The system uses a secure database with encrypted voting data.

Deployment works on cloud or local machines.

Price is two thousand US dollars, one-time payment, including full source code.

Delivery within 24 hours with free installation support and training.

Built in Haiti by GlobalInternet.py.

Let us bring Haitian elections into the digital era with a secure and modern solution.""",

    "French": """Système de vote en ligne officiel prêt pour les élections en Haïti.

GlobalInternet.py, propriété de Gesner Deslandes, a développé une plateforme de vote complète, sécurisée et multilingue construite en Python.

Ce système est proposé au gouvernement haïtien, au CEP et à toute institution électorale.

Interface multilingue en créole, français, anglais et espagnol.

Chaque électeur reçoit un identifiant unique empêchant le double vote.

Le président du CEP dispose d’un tableau de bord complet pour gérer les candidats.

Le suivi du vote se fait en temps réel avec affichage des résultats.

Des rapports PDF instantanés peuvent être générés.

Les profils des candidats incluent photos, symboles et slogans.

Une option permet de voter pour aucun candidat.

La durée du scrutin est contrôlée automatiquement.

La base de données est sécurisée avec des votes chiffrés.

Déploiement facile sur serveur cloud ou local.

Prix : 2000 dollars américains, paiement unique avec code source complet.

Livraison sous 24 heures avec assistance gratuite.

Fabriqué en Haïti par GlobalInternet.py.

Faisons entrer les élections haïtiennes dans l’ère numérique.""",

    "Spanish": """Sistema oficial de votación en línea para elecciones en Haití.

Desarrollado por GlobalInternet.py, propiedad de Gesner Deslandes.

Es una plataforma completa, segura y multilingüe construida en Python.

Diseñada para el gobierno haitiano.

Incluye múltiples idiomas y prevención de doble voto.

Panel completo para gestionar candidatos.

Seguimiento en tiempo real de votos.

Generación de reportes PDF.

Perfiles de candidatos con datos reales.

Opción de voto neutral.

Control automático del tiempo de votación.

Base de datos segura con datos cifrados.

Fácil implementación en la nube o local.

Precio: 2000 dólares, pago único.

Entrega en 24 horas con soporte.

Hecho en Haití por GlobalInternet.py.

Llevemos las elecciones haitianas a la era digital."""
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
# STREAMLIT UI
# -----------------------------
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
