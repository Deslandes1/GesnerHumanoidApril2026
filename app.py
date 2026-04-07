import streamlit as st
from PIL import Image, ImageDraw
import asyncio
import edge_tts
import time
import os
import base64

st.set_page_config(page_title="Gesner Humanoid AI - Singing", layout="wide")

# -----------------------------
# VOICE SETTINGS (fallback for spoken version)
# -----------------------------
voices = {
    "English": "en-US-GuyNeural",
    "French": "fr-FR-HenriNeural",
    "Spanish": "es-ES-AlvaroNeural"
}

# -----------------------------
# HAITIAN ANTHEM LYRICS (excerpt)
# -----------------------------
anthem_lyrics = """Pour le pays, pour les ancêtres,
Marchons unis, marchons unis.
Dans nos rangs point de traîtres,
Du sol soyons seuls maîtres.
Marchons unis, marchons unis,
Pour le pays, pour les ancêtres.

Marchons, marchons, marchons unis,
Pour le pays, pour les ancêtres."""

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
# GENERATE SPOKEN VERSION (fallback)
# -----------------------------
async def generate_spoken_audio(text, voice):
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save("voice.mp3")

# -----------------------------
# ESTIMATE DURATION FOR ANIMATION
# -----------------------------
def estimate_duration(text):
    words = len(text.split())
    # Anthem takes ~30 seconds when spoken with rhythm
    return max(25, words / 2.0)

# -----------------------------
# STREAMLIT UI WITH HAITIAN FLAG
# -----------------------------
col_flag, col_main, col_right = st.columns([1, 3, 1])

with col_flag:
    st.image("https://flagcdn.com/w320/ht.png", width=120)

with col_main:
    st.title("🤖 Gesner Humanoid AI - Sings La Dessalinienne")
    st.markdown("**Haitian National Anthem (excerpt)**")
    
    # Display lyrics
    st.markdown(f"```\n{anthem_lyrics}\n```")
    
    # Audio upload option for real singing
    uploaded_audio = st.file_uploader("🎤 Upload a singing audio file (MP3) for better rhythm", type=["mp3"])
    
    frame = st.empty()
    frame.image(create_face(False))
    
    if st.button("🎵 Sing / Recite"):
        if uploaded_audio is not None:
            # Use uploaded singing audio
            st.audio(uploaded_audio, format="audio/mp3")
            # Estimate duration from file size (rough)
            duration = len(uploaded_audio.getvalue()) / 32000  # approx 32kbps
            duration = max(25, min(duration, 45))
        else:
            # Fallback: generate spoken version with rhythm
            with st.spinner("Generating spoken version..."):
                asyncio.run(generate_spoken_audio(anthem_lyrics, voices["French"]))
                audio_file = open("voice.mp3", "rb")
                st.audio(audio_file.read(), format="audio/mp3")
                duration = estimate_duration(anthem_lyrics)
        
        # Animate mouth for the duration
        start = time.time()
        while time.time() - start < duration:
            frame.image(create_face(True))
            time.sleep(0.25)
            frame.image(create_face(False))
            time.sleep(0.25)
        frame.image(create_face(False))
        
        if not uploaded_audio:
            os.remove("voice.mp3")
    
    st.info("For the best experience, upload a recording of someone singing the anthem. The humanoid will move its lips in sync.")

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
