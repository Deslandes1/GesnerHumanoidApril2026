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
    "English": """How Engineers in Silicon Valley Build Software Today – And How We Do It at GlobalInternet.py.

I, Gesner Deslandes, the owner of GlobalInternet.py, want to share with you how software is built today and how my online company delivers working applications in record time.

In Silicon Valley, the role of an engineer has changed completely. Developers no longer spend weeks writing every line of code by hand. Instead, they focus on architecture, user experience, and problem-solving.

They describe what they want in plain English, and AI tools generate the code almost instantly.

The engineer’s job becomes breaking down problems, prompting AI, reviewing code, integrating systems, and deploying fast.

At GlobalInternet.py, I follow this exact model. I act as the architect and product owner, designing, validating, and deploying everything from the cloud.

Because my company is one hundred percent online, I deliver complete software solutions within twenty-four hours.

We deliver full-stack applications, databases, AI tools, and complete systems with documentation.

Made in Haiti, built for the world.

Let’s build something great together.""",

    "French": """Comment les ingénieurs de la Silicon Valley construisent des logiciels aujourd’hui.

Je suis Gesner Deslandes, fondateur de GlobalInternet.py.

Aujourd’hui, les développeurs utilisent l’intelligence artificielle pour créer plus rapidement.

Ils définissent les problèmes, donnent des instructions, vérifient le code et déploient rapidement.

Chez GlobalInternet.py, je travaille exactement ainsi.

Je conçois, développe et livre des applications complètes en moins de 24 heures.

Nous créons des applications web, des bases de données et des outils intelligents.

Fait en Haïti, pour le monde entier.

Construisons quelque chose de grand ensemble.""",

    "Spanish": """Cómo los ingenieros en Silicon Valley construyen software hoy.

Soy Gesner Deslandes, fundador de GlobalInternet.py.

Hoy en día, los desarrolladores usan inteligencia artificial para crear software más rápido.

Definen problemas, dan instrucciones y validan el código.

En GlobalInternet.py seguimos este mismo modelo.

Creamos aplicaciones completas en menos de 24 horas.

Desarrollamos software, bases de datos y herramientas de inteligencia artificial.

Hecho en Haití para el mundo.

Construyamos algo grande juntos."""
}

# -----------------------------
# CREATE ROBOT FACE (KEEP YOUR STYLE)
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

    # Animate based on speech duration
    duration = estimate_duration(texts[language])

    start = time.time()
    while time.time() - start < duration:
        frame.image(create_face(True))
        time.sleep(0.2)
        frame.image(create_face(False))
        time.sleep(0.2)

    frame.image(create_face(False))
