import streamlit as st
from PIL import Image, ImageDraw
import asyncio
import edge_tts
import time
import os
from mutagen.mp3 import MP3

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
# TRANSLATED LYRICS (Two parts)
# -----------------------------
lyrics_parts = {
    "First Part": {
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
    },
    "Second Part": {
        "French (original)": """Pour les Aïeux, pour la Patrie,
Bêchons joyeux, bêchons joyeux.
Quand le champ fructifie,
L'âme se fortifie.
Bêchons joyeux, bêchons joyeux,
Pour les Aïeux, pour la Patrie.

Bêchons, bêchons, bêchons joyeux,
Pour les Aïeux, pour la Patrie.""",

        "English": """For the ancestors, for the homeland,
Let us dig joyfully, let us dig joyfully.
When the field bears fruit,
The soul grows stronger.
Let us dig joyfully, let us dig joyfully,
For the ancestors, for the homeland.

Let us dig, let us dig, let us dig joyfully,
For the ancestors, for the homeland.""",

        "Spanish": """Por los ancestros, por la patria,
Cavemos alegres, cavemos alegres.
Cuando el campo fructifica,
El alma se fortalece.
Cavemos alegres, cavemos alegres,
Por los ancestros, por la patria.

Cavemos, cavemos, cavemos alegres,
Por los ancestros, por la patria."""
    }
}

# -----------------------------
# CREATE ROBOT FACE (compact)
# -----------------------------
def create_face(mouth_open=False):
    img = Image.new("RGB", (300, 300), "white")
    draw = ImageDraw.Draw(img)

    # Head
    draw.ellipse((38, 60, 262, 262), outline="black", width=4)

    # Inner face
    draw.ellipse((68, 90, 232, 240), outline="black", width=3)

    # Eyes
    draw.ellipse((105, 128, 135, 158), fill="black")
    draw.ellipse((165, 128, 195, 158), fill="black")

    # Mouth
    if mouth_open:
        draw.ellipse((128, 180, 172, 225), outline="black", width=3)
    else:
        draw.arc((115, 173, 185, 225), start=0, end=180, fill="black", width=3)

    # Antenna
    draw.line((150, 60, 150, 30), fill="black", width=3)
    draw.ellipse((139, 15, 161, 38), outline="black", width=2)

    # Side panels
    draw.rectangle((30, 135, 53, 195), outline="black", width=2)
    draw.rectangle((247, 135, 270, 195), outline="black", width=2)

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

def get_audio_duration(file_path):
    audio = MP3(file_path)
    return audio.info.length

# -----------------------------
# HIGHLIGHT LYRICS
# -----------------------------
def highlight_lyrics(text, current_line_index, lines):
    highlighted = []
    for i, line in enumerate(lines):
        if i == current_line_index:
            highlighted.append(f'<span style="color: gold; font-weight: bold;">{line}</span>')
        else:
            highlighted.append(f'<span style="color: black;">{line}</span>')
    return "<br>".join(highlighted)

# -----------------------------
# COMPACT LAYOUT
# -----------------------------
col_flag, col_humanoid, col_lyrics = st.columns([1, 1.5, 1.5])

with col_flag:
    st.image("https://flagcdn.com/w320/ht.png", width=100)

with col_humanoid:
    st.markdown("<h3 style='margin-bottom: 0;'>🤖 Gesner Humanoid AI</h3>", unsafe_allow_html=True)
    st.markdown("<p style='margin-top: 0; font-size: 0.9rem;'>La Dessalinienne – Haitian National Anthem</p>", unsafe_allow_html=True)
    
    part = st.radio("Select Part", ["First Part", "Second Part"], horizontal=True)
    language = st.selectbox("🌍 Language", list(voices.keys()), label_visibility="collapsed")
    
    frame = st.empty()
    frame.image(create_face(False), width=250)
    
    if st.button("🔊 Speak", use_container_width=True):
        selected_text = lyrics_parts[part][language]
        with st.spinner("Generating voice..."):
            generate_audio_sync(selected_text, voices[language])
            audio_file = open("speech.mp3", "rb")
            st.audio(audio_file.read(), format="audio/mp3")
            duration = get_audio_duration("speech.mp3")
            audio_file.close()
        
        # Split lyrics into lines for highlighting
        lines = selected_text.split('\n')
        num_lines = len(lines)
        time_per_line = duration / num_lines
        
        # Highlight container
        lyrics_placeholder = col_lyrics.empty()
        
        # Mouth animation + line highlighting
        start = time.time()
        line_idx = 0
        while time.time() - start < duration:
            elapsed = time.time() - start
            line_idx = min(int(elapsed / time_per_line), num_lines - 1)
            highlighted_html = highlight_lyrics(selected_text, line_idx, lines)
            lyrics_placeholder.markdown(f"<div style='font-family: monospace; font-size: 0.9rem; line-height: 1.4;'>{highlighted_html}</div>", unsafe_allow_html=True)
            
            # Animate mouth
            frame.image(create_face(True), width=250)
            time.sleep(0.2)
            frame.image(create_face(False), width=250)
            time.sleep(0.2)
        
        # Final state: no highlight, mouth closed
        lyrics_placeholder.markdown(f"<div style='font-family: monospace; font-size: 0.9rem; line-height: 1.4;'>{selected_text.replace(chr(10), '<br>')}</div>", unsafe_allow_html=True)
        frame.image(create_face(False), width=250)
        
        # Clean up
        if os.path.exists("speech.mp3"):
            os.remove("speech.mp3")

with col_lyrics:
    st.markdown("<h3 style='margin-bottom: 5px;'>📜 Lyrics</h3>", unsafe_allow_html=True)
    st.markdown(f"<p style='font-size: 0.85rem;'><b>{language}</b></p>", unsafe_allow_html=True)
    # Initially show first part lyrics
    default_text = lyrics_parts["First Part"][language]
    st.markdown(f"<div style='font-family: monospace; font-size: 0.9rem; line-height: 1.4;'>{default_text.replace(chr(10), '<br>')}</div>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("""
    <div style='text-align: right; font-size: 0.8rem;'>
        <b>GlobalInternet.py</b><br>
        Gesner Deslandes<br>
        Python Developer
    </div>
    """, unsafe_allow_html=True)

st.markdown("© 2026 GlobalInternet.py – All rights reserved")
