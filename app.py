import streamlit as st
from PIL import Image, ImageDraw
import asyncio
import edge_tts
import time
from mutagen.mp3 import MP3
import base64
import os
import tempfile

# 1. PAGE CONFIG & NO-SCROLL CSS
st.set_page_config(layout="wide", page_title="Gesner Humanoid AI")

st.markdown("""
    <style>
        .block-container { padding-top: 0.5rem; padding-bottom: 0rem; }
        [data-testid="stVerticalBlock"] { gap: 0.2rem; }
        img { max-width: 100%; height: auto; border-radius: 50%; }
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# 2. VOICES & SCRIPTS
voices = {"English": "en-US-GuyNeural", "French": "fr-FR-HenriNeural"}
promo_script_en = "Attention! This is Gesner Humanoid AI. Ariana, your courage and joy represent the very best of Haiti! Haiti stands tall because of you!"
promo_script_fr = "Attention ! Ici l'IA Humanoïde Gesner. Ariana, ton courage et ta joie représentent le meilleur d'Haïti ! Haïti est fière de toi !"
texts = {"English": promo_script_en, "French": promo_script_fr}

# 3. FACE DESIGN
def create_face(is_open=False):
    img = Image.new("RGB", (400, 400), "white")
    draw = ImageDraw.Draw(img)
    draw.ellipse((50, 80, 350, 350), outline="black", width=5)
    draw.ellipse((140, 170, 180, 210), fill="black")
    draw.ellipse((220, 170, 260, 210), fill="black")
    center_y = 265
    if is_open:
        draw.ellipse((110, center_y - 50, 290, center_y + 50), fill="black")
    else:
        draw.line((140, center_y, 260, center_y), fill="black", width=22)
    return img

# 4. HEADER
h_col1, h_col2 = st.columns([1, 10])
with h_col1: st.markdown("<h1 style='margin-top: -15px;'>🇭🇹</h1>", unsafe_allow_html=True)
with h_col2: st.markdown("<h2 style='margin-top: -10px;'>Gesner Humanoid AI</h2>", unsafe_allow_html=True)

# 5. MAIN LAYOUT
left, right = st.columns([2, 1])

with left:
    language = st.selectbox("🌍 Select Language", list(voices.keys()))
    face_placeholder = st.empty()
    face_placeholder.image(create_face(is_open=False), width=350)
    audio_placeholder = st.empty()
    start_btn = st.button("🚀 Start Announcement", use_container_width=True)

with right:
    # Branding
    st.markdown('<div style="background-color: #003366; padding: 10px; border-radius: 8px; text-align: center; color: white;"><b>GLOBALINTERNET.PY</b></div>', unsafe_allow_html=True)
    
    # IMAGE FIX: We use a robust URL format and a fallback
    # In GitHub, a file named "Ariana .png" is often referenced as "Ariana%20.png" 
    # but the safest way is to rename the file in your GitHub to "Ariana.png" (no space).
    ariana_url = "https://raw.githubusercontent.com/deslandes78/gesnerhumanoidapril2026/main/Ariana%20.png"
    
    st.markdown(f"""
        <div style="background-color: #fdfdfd; padding: 10px; border-radius: 10px; text-align: center; border: 3px solid #003366; margin-top: 10px;">
            <div style="width: 140px; height: 140px; border-radius: 50%; border: 3px solid #003366; overflow: hidden; margin: 0 auto; background-color: #eee;">
                <img src="{ariana_url}" onerror="this.src='https://via.placeholder.com/150?text=Ariana'" style="width: 100%; height: 100%; object-fit: cover;">
            </div>
            <p style="font-weight: bold; color: #003366; margin-top: 5px;">ARIANA</p>
            <p style="font-size: 0.7em;">Courage • Joy • Pride</p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("📱 **(509) 4738-5663**")

# 6. EXECUTION
if start_btn:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
        audio_path = tmp.name
    asyncio.run(edge_tts.Communicate(texts[language], voices[language]).save(audio_path))
    duration = MP3(audio_path).info.length
    with open(audio_path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode()
    audio_placeholder.markdown(f'<audio autoplay="true"><source src="data:audio/mp3;base64,{b64}"></audio>', unsafe_allow_html=True)
    
    start_time = time.time()
    toggle = True
    while (time.time() - start_time) < duration:
        face_placeholder.image(create_face(is_open=toggle), width=350)
        toggle = not toggle
        time.sleep(0.05)
    face_placeholder.image(create_face(is_open=False), width=350)
    if os.path.exists(audio_path): os.remove(audio_path)
