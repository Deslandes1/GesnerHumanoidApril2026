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
# PAGE CONFIG - FORCED COMPACT FOR VIDEO
# -----------------------------
st.set_page_config(layout="wide", page_title="Gesner Humanoid AI")

# CSS to remove padding and ensure "one-screen" fit
st.markdown("""
    <style>
        .block-container { padding-top: 1rem; padding-bottom: 0rem; }
        [data-testid="stVerticalBlock"] { gap: 0.5rem; }
    </style>
""", unsafe_allow_html=True)

# -----------------------------
# ASSETS & SCRIPT
# -----------------------------
voices = {"English": "en-US-AriaNeural", "French": "fr-FR-DeniseNeural"}

promo_script_en = """
This is Gesner Humanoid AI with a special message of joy and pride!
Ariana, your courage and your infectious joy as you represent Haiti in Africa inspire us all!
May your parents and your twin sister be bursting with pride! Haiti stands tall because of you!
Keep going, Ariana! We are with you! This is Gesner Humanoid AI for GlobalInternet.py.
"""

promo_script_fr = """
Ici l'IA Humanoïde Gesner pour un message de fierté !
Ariana, ton courage et ta joie alors que tu représentes Haïti en Afrique nous inspirent tous !
Que tes parents et ta sœur jumelle soient remplis de fierté ! Haïti est fière de toi !
Continue, Ariana ! Nous sommes avec toi ! C'était l'IA Humanoïde Gesner pour GlobalInternet.py.
"""

texts = {"English": promo_script_en, "French": promo_script_fr}

# -----------------------------
# FACE DESIGN (AGGRESSIVE MOUTH)
# -----------------------------
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

# -----------------------------
# UI LAYOUT
# -----------------------------
# Top row for Flag and Title
col_flag, col_title = st.columns([1, 5])
with col_flag:
    st.markdown("# 🇭🇹") # Haitian Flag positioned Top-Left
with col_title:
    st.title("Gesner Humanoid AI")

left, right = st.columns([2, 1])

with left:
    language = st.selectbox("🌍 Select Language", list(voices.keys()))
    face_placeholder = st.empty()
    face_placeholder.image(create_face(is_open=False), width=350)
    audio_placeholder = st.empty()
    
    start_btn = st.button("🚀 Start Announcement")

with right:
    # Company Branding (Compact)
    st.markdown("""
        <div style="background-color: #003366; padding: 10px; border-radius: 8px; text-align: center;">
            <h4 style="color: white; margin: 0;">GLOBALINTERNET.PY</h4>
            <p style="color: #66ccff; font-size: 0.8em; margin:0;">Gesner Deslandes | Founder</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Ariana Celebration Component (Using GitHub link)
    # Note: Using the provided name "Ariana .png" as per your request
    ariana_url = "https://raw.githubusercontent.com/your-username/your-repo/main/Ariana%20.png"
    
    st.markdown(f"""
        <div style="background-color: #f0f8ff; padding: 10px; border-radius: 10px; text-align: center; border: 3px solid #003366; margin-top: 10px;">
            <div style="position: relative;">
                <span style="color: blue;">💙</span> <span style="color: red;">❤️</span>
                <div style="width: 120px; height: 120px; border-radius: 50%; border: 3px solid #003366; overflow: hidden; margin: 5px auto;">
                    <img src="{ariana_url}" style="width: 100%; height: 100%; object-fit: cover;" onerror="this.src='https://via.placeholder.com/120?text=Ariana'">
                </div>
                <p style="font-weight: bold; margin:0; color: #003366;">ARIANA</p>
                <p style="font-size: 0.7em; margin:0;">Courage • Joy • Patience</p>
                <div style="font-size: 1.5em; margin-top: 5px;">🎈🎈🎈</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("""
        <div style="font-size: 0.8em; line-height: 1.2; margin-top: 10px;">
            📱 (509) 4738-5663<br>
            📧 deslandes78@gmail.com
        </div>
    """, unsafe_allow_html=True)

# -----------------------------
# EXECUTION ENGINE
# -----------------------------
if start_btn:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
        audio_path = tmp.name
    
    with st.spinner("Preparing..."):
        asyncio.run(edge_tts.Communicate(texts[language], voices[language]).save(audio_path))
    
    with open(audio_path, "rb") as f:
        audio_bytes = f.read()
        b64 = base64.b64encode(audio_bytes).decode()
    
    duration = MP3(audio_path).info.length
    
    audio_html = f"""
        <audio autoplay="true">
            <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
        </audio>
    """
    audio_placeholder.markdown(audio_html, unsafe_allow_html=True)
    
    # Aggressive animation loop synced to audio duration
    start_time = time.time()
    toggle = True
    while (time.time() - start_time) < duration:
        face_placeholder.image(create_face(is_open=toggle), width=350)
        toggle = not toggle
        time.sleep(0.05) # Intense speed
    
    face_placeholder.image(create_face(is_open=False), width=350)
    
    if os.path.exists(audio_path):
        os.remove(audio_path)
