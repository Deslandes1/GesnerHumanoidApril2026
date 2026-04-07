import streamlit as st
from PIL import Image, ImageDraw
import asyncio
import edge_tts
import time
import os

st.set_page_config(page_title="Gesner Humanoid AI - La Dessalinienne", layout="wide")

# -----------------------------
# VOICE SETTINGS
# -----------------------------
voices = {
    "French (original)": "fr-FR-HenriNeural",
    "English": "en-US-GuyNeural",
    "Spanish": "es-ES-AlvaroNeural"
}

# -----------------------------
# TRANSLATED LYRICS
# -----------------------------
lyrics = {
    "French (original)": """Pour le pays, pour les ancêtres,
Marchons unis, marchons unis.
Dans nos rangs point de traîtres,
Du sol soyons seuls maîtres.
Marchons unis, marchons unis,
Pour le pays, pour les ancêtres.

Marchons, marchons, marchons unis,
Pour le pays, pour les ancêtres.""",

    "English": """For the country, for the ancestors,
Let us march united, let us march united.
In our ranks no traitors,
Let us be the sole masters of the soil.
Let us march united, let us march united,
For the country, for the ancestors.

Let us march, let us march, let us march united,
For the country, for the ancestors.""",

    "Spanish": """Por el país, por los ancestros,
Marchemos unidos, marchemos unidos.
En nuestras filas no hay traidores,
Seamos los únicos dueños del suelo.
Marchemos unidos, marchemos unidos,
Por el país, por los ancestros.

Marchemos, marchemos, marchemos unidos,
Por el país, por los ancestros."""
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

    # Mouth
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
# SYNCHRONOUS AUDIO GENERATION
# -----------------------------
def generate_audio_sync(text, voice):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        communicate = edge_tts.Communicate(text, voice)
        loop.run_until_complete(communicate.save("speech.mp3"))
    finally:
        loop.close()

def estimate_duration(text):
    words = len(text.split())
    return max(8, words / 2.2)

# -----------------------------
# STREAMLIT UI WITH HAITIAN FLAG
# -----------------------------
col_flag, col_main, col_right = st.columns([1, 3, 1])

with col_flag:
    st.image("https://flagcdn.com/w320/ht.png", width=120)

with col_main:
    st.title("🤖 Gesner Humanoid AI")
    st.markdown("### La Dessalinienne – Haitian National Anthem")

    language = st.selectbox("🌍 Select language for recitation", list(voices.keys()))
    st.markdown(f"**Lyrics ({language}):**")
    st.text(lyrics[language])

    frame = st.empty()
    frame.image(create_face(False))

    if st.button("🔊 Recite"):
        with st.spinner("Generating voice..."):
            generate_audio_sync(lyrics[language], voices[language])
            audio_file = open("speech.mp3", "rb")
            st.audio(audio_file.read(), format="audio/mp3")
            duration = estimate_duration(lyrics[language])
            audio_file.close()

        # Animate mouth
        start = time.time()
        while time.time() - start < duration:
            frame.image(create_face(True))
            time.sleep(0.2)
            frame.image(create_face(False))
            time.sleep(0.2)
        frame.image(create_face(False))

        # Clean up
        if os.path.exists("speech.mp3"):
            os.remove("speech.mp3")

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
