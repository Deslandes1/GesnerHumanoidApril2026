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
# 1. PAGE CONFIG & NO-SCROLL CSS
# -----------------------------
st.set_page_config(layout="wide", page_title="Gesner Humanoid AI")

st.markdown("""
    <style>
        /* Force everything into one screen for video recording */
        .block-container { padding-top: 0.5rem; padding-bottom: 0rem; }
        [data-testid="stVerticalBlock"] { gap: 0.2rem; }
        .stSelectbox { margin-bottom: -1rem; }
        img { max-width: 100%; height: auto; }
        /* Hide the Streamlit footer and hamburger menu for a cleaner screenshot */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# -----------------------------
# 2. VOICES & SCRIPTS
# -----------------------------
voices = {"English": "en-US-GuyNeural", "French": "fr-FR-HenriNeural"}

promo_script_en = """
Attention! This is Gesner Humanoid AI with a special message for Ariana! 
Ariana, your courage and joy represent the very best of Haiti. 
May your parents and your twin sister be filled with pride as you represent us in Africa! 
Haiti stands tall because of you. This is Gesner Humanoid AI for GlobalInternet.py. 
Keep going, Ariana! We are with you!
"""

promo_script_fr = """
Attention ! Ici l'IA Humanoïde Gesner pour un message spécial pour Ariana ! 
Ariana, ton courage et ta joie représentent le meilleur d'Haïti. 
Que tes parents et ta sœur jumelle soient remplis de fierté alors que tu nous représentes en Afrique ! 
Haïti est fière de toi. C'était l'IA Humanoïde Gesner pour GlobalInternet.py. 
Continue, Ariana ! Nous sommes avec toi !
"""

texts = {"English": promo_script_en, "French": promo_script_fr}

# -----------------------------
# 3. FACE DESIGN (AGGRESSIVE MOUTH)
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
        draw.line((140, center_y, 260, center_y), fill="black", width=22)
        
    draw.line((200, 40, 200, 80), fill="black", width=4)
    draw.ellipse((185, 20, 215, 50), outline="black", width=3)
    return img

# -----------------------------
# 4. TOP HEADER (FLAG + TITLE)
# -----------------------------
# Positioned specifically at the top left as requested
header_col1, header_col2 = st.columns([1, 10])
with header_col1:
    st.markdown("<h1 style='margin-top: -15px;'>🇭🇹</h1>", unsafe_allow_html=True)
with header_col2:
    st.markdown("<h2 style='margin-top: -10px;'>Gesner Humanoid AI</h2>", unsafe_allow_html=True)

# -----------------------------
# 5. MAIN UI LAYOUT
# -----------------------------
left, right = st.columns([2, 1])

with left:
    language = st.selectbox("🌍 Select Language", list(voices.keys()))
    face_placeholder = st.empty()
    face_placeholder.image(create_face(is_open=False), width=350)
    audio_placeholder = st.empty()
    start_btn = st.button("🚀 Start Announcement", use_container_width=True)

with right:
    # Branding
    st.markdown("""
        <div style="background-color: #003366; padding: 10px; border-radius: 8px; text-align: center; border: 1px solid #66ccff;">
            <h4 style="color: white; margin: 0; font-size: 1em;">GLOBALINTERNET.PY</h4>
            <p style="color: #66ccff; font-size: 0.7em; margin:0;">Gesner Deslandes | Founder</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Ariana Profile Image from GitHub
    ariana_url = "https://raw.githubusercontent.com/deslandes78/gesnerhumanoidapril2026/main/Ariana%20.png"
    
    st.markdown(f"""
        <div style="background-color: #fdfdfd; padding: 8px; border-radius: 10px; text-align: center; border: 3px solid #003366; margin-top: 8px;">
            <span style="color: blue;">💙</span> <span style="color: red;">❤️</span>
            <div style="width: 120px; height: 120px; border-radius: 50%; border: 3px solid #003366; overflow: hidden; margin: 5px auto;">
                <img src="{ariana_url}" style="width: 100%; height: 100%; object-fit: cover;">
            </div>
            <p style="font-weight: bold; margin:0; color: #003366; font-size: 0.9em;">ARIANA</p>
            <p style="font-size: 0.65em; margin:0; font-weight: 600;">Courage • Joy • Patience</p>
            <div style="font-size: 1.2em; margin-top: 2px;">🎈🎈🎈</div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("""
        <div style="font-size: 0.75em; line-height: 1.2; margin-top: 8px; border-left: 3px solid #003366; padding-left: 8px;">
            <b>📱 (509) 4738-5663</b><br>
            📧 deslandes78@gmail.com
        </div>
    """, unsafe_allow_html=True)

# -----------------------------
# 6. ANIMATION & AUDIO EXECUTION
# -----------------------------
if start_btn:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
        audio_path = tmp.name
    
    with st.spinner("Generating..."):
        asyncio.run(edge_tts.Communicate(texts[language], voices[language]).save(audio_path))
    
    # Get audio duration
    duration = MP3(audio_path).info.length
    
    with open(audio_path, "rb") as f:
        audio_bytes = f.read()
        b64 = base64.b64encode(audio_bytes).decode()
    
    # Audio play
    audio_html = f"""
        <audio autoplay="true">
            <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
        </audio>
    """
    audio_placeholder.markdown(audio_html, unsafe_allow_html=True)
    
    # Aggressive animation loop synced to audio length
    start_time = time.time()
    toggle = True
    while (time.time() - start_time) < duration:
        face_placeholder.image(create_face(is_open=toggle), width=350)
        toggle = not toggle
        time.sleep(0.05) # Intense toggle speed
    
    # Reset
    face_placeholder.image(create_face(is_open=False), width=350)
    
    if os.path.exists(audio_path):
        os.remove(audio_path)
