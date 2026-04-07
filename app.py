import streamlit as st
from PIL import Image, ImageDraw
import asyncio
import edge_tts
import time

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(layout="centered")

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

This system is designed for the Haitian government, the CEP, and any electoral institution to modernize elections with transparency, accessibility, and real-time results.

Key features include multilingual interface in Creole, French, English, and Spanish.

Each voter receives a unique ID to prevent double voting.

The CEP President has full control through a powerful dashboard to manage candidates, including adding, updating, and removing profiles.

Votes are tracked in real time, showing live results and current leaders.

Instant PDF reports can be generated for media, observers, and public release.

Candidate profiles include authentic images, party symbols, and slogans.

A neutral voting option allows citizens to select no candidate.

Election duration can be controlled with automatic closing.

The system uses a secure database with encrypted voting data.

Deployment is simple and works on cloud or local machines.

Price for the Haitian government is two thousand US dollars, one-time payment, including full source code and lifetime usage.

Delivery is within 24 hours with free remote installation support and training.

Built in Haiti by GlobalInternet.py.

Let us bring Haitian elections into the digital era with a secure and modern solution.""",

    "French": """Système de vote en ligne officiel prêt pour les élections en Haïti.

GlobalInternet.py, propriété de Gesner Deslandes, a développé une plateforme de vote complète, sécurisée et multilingue construite en Python.

Ce système est proposé au gouvernement haïtien, au CEP ou à toute institution électorale pour moderniser le processus de vote et garantir transparence, accessibilité et résultats en temps réel.

Fonctionnalités clés : interface multilingue en créole, français, anglais et espagnol.

Chaque électeur reçoit un identifiant unique empêchant le double vote.

Le président du CEP dispose d’un tableau de bord complet pour gérer les candidats, incluant l’ajout, la mise à jour et la suppression.

Le suivi du scrutin se fait en temps réel avec affichage du leader et des résultats.

Des rapports PDF instantanés peuvent être générés pour les médias et les observateurs.

Les profils des candidats incluent photos, symboles, partis et slogans.

Une option permet de voter pour aucun candidat.

La durée du scrutin est contrôlée automatiquement avec arrêt du vote.

La base de données est sécurisée avec des votes chiffrés.

Le système est facile à déployer sur serveur cloud ou local.

Prix : 2000 dollars américains, paiement unique incluant le code source complet et utilisation illimitée.

Livraison sous 24 heures avec assistance et formation gratuites.

Fabriqué en Haïti par GlobalInternet.py.

Faisons entrer les élections haïtiennes dans l’ère numérique avec une solution moderne et sécurisée.""",

    "Spanish": """Sistema oficial de votación en línea para elecciones en Haití.

Desarrollado por GlobalInternet.py, propiedad de Gesner Deslandes.

Hemos creado una plataforma completa, segura y multilingüe construida en Python.

Diseñada para el gobierno haitiano y autoridades electorales para modernizar el proceso con transparencia y resultados en tiempo real.

Incluye múltiples idiomas: criollo, francés, inglés y español.

Cada votante recibe un ID único para evitar duplicación.

El presidente del CEP tiene control total para gestionar candidatos.

Seguimiento en tiempo real de votos y resultados.

Generación instantánea de reportes PDF.

Perfiles de candidatos con imágenes, símbolos y eslóganes.

Opción de voto neutral.

Control automático del tiempo de votación.

Base de datos segura con datos cifrados.

Fácil implementación en la nube o local.

Precio: 2000 dólares, pago único con acceso completo.

Entrega en 24 horas con soporte y formación.

Hecho en Haití por GlobalInternet.py.

Llevemos las elecciones haitianas a la era digital."""
}

# -----------------------------
# ORIGINAL HUMANOID FACE
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
# ESTIMATE DURATION
# -----------------------------
def estimate_duration(text):
    return len(text.split()) / 2.5

# -----------------------------
# UI
# -----------------------------
st.title("🤖 Gesner Humanoid AI")

# 🇭🇹 FLAG
st.markdown(
    "<div style='text-align:center;'><img src='https://upload.wikimedia.org/wikipedia/commons/5/56/Flag_of_Haiti.svg' width='120'></div>",
    unsafe_allow_html=True
)

# Language selector
language = st.selectbox("🌍 Select Language", list(voices.keys()))

# Face display
frame = st.empty()
frame.image(create_face(False))

# Speak button
if st.button("▶️ Speak"):

    asyncio.run(generate_voice(texts[language], voices[language]))

    audio_file = open("voice.mp3", "rb")
    st.audio(audio_file.read(), format="audio/mp3")

    duration = estimate_duration(texts[language])

    start = time.time()
    while time.time() - start < duration:
        frame.image(create_face(True))
        time.sleep(0.2)
        frame.image(create_face(False))
        time.sleep(0.2)

    frame.image(create_face(False))
