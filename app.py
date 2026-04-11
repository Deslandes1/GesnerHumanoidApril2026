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

# New congratulatory script for Ariana
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
# HAITIAN FLAG FUNCTION (blue/red blocks + emoji)
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
    # Face Structure
    draw.ellipse((50, 80, 350, 350), outline="black", width=5)
    draw.ellipse((90, 120, 310, 320), outline="black", width=3)
    # Eyes
    draw.ellipse((140, 170, 180, 210), fill="black")
    draw.ellipse((220, 170, 260, 210), fill="black")
    
    # --- AGGRESSIVE MOUTH MOVEMENT ---
    center_y = 265
    if is_open:
        # Extra Large, aggressive open mouth
        draw.ellipse((110, center_y - 50, 290, center_y + 50), fill="black")
    else:
        # Very thick, heavy aggressive closed line
        draw.line((140, center_y, 260, center_y), fill="black", width=20)
        
    # Antenna
    draw.line((200, 40, 200, 80), fill="black", width=4)
    draw.ellipse((185, 20, 215, 50), outline="black", width=3)
    return img

# -----------------------------
# UI LAYOUT
# -----------------------------
left, right = st.columns([3, 1])

with right:
    # HAITIAN FLAG (original position)
    show_haitian_flag()
    
    # Company branding
    st.markdown("---")
    st.markdown("""
        <div style="background-color: #003366; padding: 20px; border-radius: 10px; text-align: center;">
            <h2 style="color: white; margin: 0;">GlobalInternet.py</h2>
            <p style="color: #66ccff; font-size: 0.9em;">Innovation & Tech</p>
        </div>
    """, unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("**Builder & Founder:**")
    st.markdown("### Gesner Deslandes")
    st.markdown("📱 (509) 4738-5663")
    st.markdown("📧 deslandes78@gmail.com")
    st.markdown("🔗 [Main Platform](https://globalinternetsitepy-abh7v6tnmskxxnuplrdcgk.streamlit.app/)")
    st.success("Building the Future 🇭🇹")

with left:
    st.title("🤖 Gesner Humanoid AI")
    st.subheader("🎉 Congratulatory Message: Ariana – Haiti’s Pride in Africa")
    
    # Display Ariana's picture with decorative stars and balloons
    ariana_path = "Ariana.png"
    if os.path.exists(ariana_path):
        # Create a row with columns to center the image and decorations
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            # Decorative elements: blue and red stars/balloons around the image
            st.markdown("""
                <div style="text-align: center;">
                    <span style="font-size: 40px;">🎈🔵🔴🎈</span><br>
                    <span style="font-size: 30px;">⭐️🔵⭐️🔴⭐️</span>
                </div>
            """, unsafe_allow_html=True)
            st.image(ariana_path, caption="Ariana – Our Haitian Hero", use_column_width=True)
            st.markdown("""
                <div style="text-align: center;">
                    <span style="font-size: 30px;">⭐️🔴⭐️🔵⭐️</span><br>
                    <span style="font-size: 40px;">🎈🔴🔵🎈</span>
                </div>
            """, unsafe_allow_html=True)
            # Encouragement text
            st.markdown("""
                <div style="text-align: center; background-color: #f0f0f0; padding: 10px; border-radius: 10px; margin-top: 10px;">
                    <p style="color: #00209F; font-weight: bold;">💙 Courage, Joy, Patience 💙</p>
                    <p style="color: #DE2119; font-weight: bold;">❤️ May your parents be proud! ❤️</p>
                    <p style="color: #00209F; font-weight: bold;">💙 May your twin sister be proud! 💙</p>
                    <p style="color: #DE2119; font-weight: bold;">❤️ May all of Haiti be proud! ❤️</p>
                </div>
            """, unsafe_allow_html=True)
    else:
        st.warning("Ariana.png not found. Please upload the image to the repository.")
    
    st.markdown("---")
    
    language = st.selectbox("🌍 Select Language", list(voices.keys()))
    
    face_placeholder = st.empty()
    face_placeholder.image(create_face(is_open=False))
    
    audio_placeholder = st.empty()

    if st.button("🚀 Play Congratulatory Message"):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
            audio_path = tmp.name
        
        with st.spinner("Generating audio message..."):
            asyncio.run(edge_tts.Communicate(texts[language], voices[language]).save(audio_path))
        
        with open(audio_path, "rb") as f:
            audio_bytes = f.read()
            b64 = base64.b64encode(audio_bytes).decode()
        
        duration = MP3(audio_path).info.length
        
        # Audio player
        audio_html = f"""
            <audio autoplay="true" controls style="width: 100%;">
                <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
            </audio>
        """
        audio_placeholder.markdown(audio_html, unsafe_allow_html=True)
        
        # --- AGGRESSIVE MOUTH ANIMATION FOR FULL DURATION ---
        start_time = time.time()
        toggle = True
        
        while (time.time() - start_time) < duration:
            face_placeholder.image(create_face(is_open=toggle))
            toggle = not toggle
            # Fast toggle for intense aggressive look
            time.sleep(0.04) 
        
        # Reset to closed mouth
        face_placeholder.image(create_face(is_open=False))
        
        if os.path.exists(audio_path):
            os.remove(audio_path)

# Optional footer
st.markdown("---")
st.markdown("🇭🇹 *Gesner Humanoid AI – Celebrating Haitian excellence everywhere.* 🇭🇹")
