import streamlit as st
from PIL import Image, ImageDraw
import asyncio
import edge_tts
import time
from mutagen.mp3 import MP3
import base64
import os
import tempfile
import requests
from io import BytesIO

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(layout="wide", page_title="Gesner Humanoid AI")

# -----------------------------
# VOICES & CONGRATULATORY SCRIPT
# -----------------------------
voices = {
    "English": "en-US-GuyNeural",
    "French": "fr-FR-HenriNeural"
}

congrats_script_en = """
Attention! This is Gesner Humanoid AI with a very special message!

Today we celebrate Ariana! A daughter of Haiti who is making our nation proud in Africa. 
Ariana, your courage, your joy, and your patience shine like a thousand stars. 
You carry the spirit of Haiti wherever you go. 
May your parents be proud. May your twin sister be proud. And may all of Haiti be proud of you!

You are a symbol of hope and strength. Keep going, keep shining, keep representing Haiti with excellence. 
We are all behind you, cheering you on with blue and red balloons and stars! 
This is Gesner Humanoid AI, saluting Ariana – a true Haitian hero. 
Haiti stands with you! Allez Ariana!
"""

congrats_script_fr = """
Attention ! Ici l'IA Humanoïde Gesner pour un message très spécial !

Aujourd'hui nous célébrons Ariana ! Une fille d'Haïti qui rend notre nation fière en Afrique. 
Ariana, ton courage, ta joie et ta patience brillent comme mille étoiles. 
Tu portes l'esprit d'Haïti partout où tu vas. 
Que tes parents soient fiers. Que ta sœur jumelle soit fière. Et que tout Haïti soit fier de toi !

Tu es un symbole d'espoir et de force. Continue, continue de briller, continue de représenter Haïti avec excellence. 
Nous sommes tous derrière toi, t'encourageant avec des ballons et des étoiles bleus et rouges ! 
C'est l'IA Humanoïde Gesner, saluant Ariana – une véritable héroïne haïtienne. 
Haïti est avec toi ! Allez Ariana !
"""

texts = {
    "English": congrats_script_en,
    "French": congrats_script_fr
}

# -----------------------------
# HAITIAN FLAG FUNCTION
# -----------------------------
def show_haitian_flag():
    st.markdown(
        """
        <div style="display: flex; align-items: center; justify-content: center; margin: 10px 0;">
            <div style="background-color: #00209F; width: 60px; height: 40px;"></div>
            <div style="background-color: #DE2119; width: 60px; height: 40px;"></div>
            <span style="font-size: 30px; margin-left: 10px;">🇭🇹</span>
        </div>
        """,
        unsafe_allow_html=True
    )
    st.caption("Haitian Flag (blue & red with coat of arms)")

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
# LOAD ARIANA IMAGE
# -----------------------------
def load_ariana_image():
    local_path = "Ariana .png"
    if os.path.exists(local_path):
        return Image.open(local_path)
    else:
        url = "https://raw.githubusercontent.com/Deslandes1/GesnerHumanoidApril2026/main/Ariana%20.png"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                return Image.open(BytesIO(response.content))
            else:
                return None
        except:
            return None

# -----------------------------
# MAIN LAYOUT – COMPACT, NO SCROLLING
# -----------------------------
# Top row: title
st.title("🤖 Gesner Humanoid AI")
st.subheader("🎉 Congratulatory Message: Ariana – Haiti’s Pride in Africa")

# Two main columns: left for face + Ariana, right for flag + company info
left_col, right_col = st.columns([2.5, 1.2])

with left_col:
    # Row 1: Face and Ariana side by side
    col_face, col_ariana = st.columns(2)
    with col_face:
        face_placeholder = st.empty()
        face_placeholder.image(create_face(is_open=False), width=350)
    with col_ariana:
        ariana_img = load_ariana_image()
        if ariana_img is not None:
            # Decorative stars and balloons above and below Ariana
            st.markdown(
                """
                <div style="text-align: center;">
                    <span style="font-size: 35px;">🎈🔵🔴🎈</span><br>
                    <span style="font-size: 25px;">⭐️🔵⭐️🔴⭐️</span>
                </div>
                """,
                unsafe_allow_html=True
            )
            st.image(ariana_img, caption="Ariana – Our Haitian Hero", width=280)
            st.markdown(
                """
                <div style="text-align: center;">
                    <span style="font-size: 25px;">⭐️🔴⭐️🔵⭐️</span><br>
                    <span style="font-size: 35px;">🎈🔴🔵🎈</span>
                </div>
                """,
                unsafe_allow_html=True
            )
            # Encouragement text
            st.markdown(
                """
                <div style="text-align: center; background-color: #f0f0f0; padding: 5px; border-radius: 10px; margin-top: 5px;">
                    <p style="color: #00209F; font-weight: bold; margin: 0;">💙 Courage, Joy, Patience 💙</p>
                    <p style="color: #DE2119; font-weight: bold; margin: 0;">❤️ May your parents be proud! ❤️</p>
                    <p style="color: #00209F; font-weight: bold; margin: 0;">💙 May your twin sister be proud! 💙</p>
                    <p style="color: #DE2119; font-weight: bold; margin: 0;">❤️ May all of Haiti be proud! ❤️</p>
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            st.error("Ariana image not found.")
    
    # Row 2: language selector and button (compact)
    col_lang, col_btn = st.columns([1, 1])
    with col_lang:
        language = st.selectbox("🌍 Select Language", list(voices.keys()))
    with col_btn:
        st.write("")  # spacer
        st.write("")
        play_button = st.button("🚀 Play Congratulatory Message", use_container_width=True)
    
    # Audio placeholder (below button)
    audio_placeholder = st.empty()

with right_col:
    show_haitian_flag()
    st.markdown("---")
    st.markdown(
        """
        <div style="background-color: #003366; padding: 15px; border-radius: 10px; text-align: center;">
            <h2 style="color: white; margin: 0;">GlobalInternet.py</h2>
            <p style="color: #66ccff; font-size: 0.9em;">Innovation & Tech</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    st.markdown("---")
    st.markdown("**Builder & Founder:**")
    st.markdown("### Gesner Deslandes")
    st.markdown("📱 (509) 4738-5663")
    st.markdown("📧 deslandes78@gmail.com")
    st.markdown("🔗 [Main Platform](https://globalinternetsitepy-abh7v6tnmskxxnuplrdcgk.streamlit.app/)")
    st.success("Building the Future 🇭🇹")

# -----------------------------
# AUDIO AND ANIMATION LOGIC
# -----------------------------
if play_button:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
        audio_path = tmp.name
    with st.spinner("Generating audio message..."):
        asyncio.run(edge_tts.Communicate(texts[language], voices[language]).save(audio_path))
    with open(audio_path, "rb") as f:
        audio_bytes = f.read()
        b64 = base64.b64encode(audio_bytes).decode()
    duration = MP3(audio_path).info.length
    audio_html = f"""
        <audio autoplay="true" controls style="width: 100%;">
            <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
        </audio>
    """
    audio_placeholder.markdown(audio_html, unsafe_allow_html=True)
    
    # Aggressive mouth animation for full duration
    time.sleep(0.3)  # small delay to let audio start
    start_time = time.time()
    toggle = True
    while (time.time() - start_time) < duration:
        face_placeholder.image(create_face(is_open=toggle), width=350)
        toggle = not toggle
        time.sleep(0.04)
    face_placeholder.image(create_face(is_open=False), width=350)
    
    if os.path.exists(audio_path):
        os.remove(audio_path)

# Optional footer (will be at bottom but likely out of view; you can remove if needed)
st.markdown("---")
st.markdown("🇭🇹 *Gesner Humanoid AI – Celebrating Haitian excellence everywhere.* 🇭🇹")
