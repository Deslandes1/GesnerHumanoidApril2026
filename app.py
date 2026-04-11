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
    "English": "en-US-AriaNeural", # A more appropriate voice for a celebratory script
    "French": "fr-FR-DeniseNeural" # A pleasant French alternative
}

# Revised celebratory script for Ariana
promo_script_en = """
This is Gesner Humanoid AI with a special message of joy and pride!
We are here to congratulate Ariana on her incredible journey!
Ariana, your courage, your infectious joy, and your unshakable patience as you represent our beloved Haiti in Africa are an inspiration to us all!
You are carrying our culture, our spirit, and our strength to a new continent, and you are doing it with such grace.
May your parents be bursting with pride! May your twin sister be filled with pride! And may all of Haiti stand tall and be proud of you!
Your journey is not just your own; it is a testament to the resilience and spirit of our people.
To everyone listening: Let us celebrate this remarkable ambassador! Ariana, we are with you every step of the way!
This is Gesner Humanoid AI for GlobalInternet.py, honoring our own. May Haiti always be proud!
"""

promo_script_fr = """
Ici l'IA Humanoïde Gesner pour un message spécial de joie et de fierté !
Nous sommes ici pour féliciter Ariana pour son incroyable voyage !
Ariana, ton courage, ta joie contagieuse et ta patience inébranlable alors que tu représentes notre chère Haïti en Afrique sont une source d'inspiration pour nous tous !
Tu portes notre culture, notre esprit et notre force vers un nouveau continent, et tu le fais avec tant de grâce.
Que tes parents soient remplis de fierté ! Que ta sœur jumelle soit remplie de fierté ! Et que toute Haïti se tienne debout et soit fière de toi !
Ton voyage n'est pas seulement le tien ; c'est un témoignage de la résilience et de l'esprit de notre peuple.
À tous ceux qui nous écoutent : Célébrons cette remarquable ambassadrice ! Ariana, nous sommes avec toi à chaque étape !
C'était l'IA Humanoïde Gesner pour GlobalInternet.py, honorant les nôtres. Que Haïti soit toujours fière !
"""

texts = {
    "English": promo_script_en,
    "French": promo_script_fr
}

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
# ARIANA CELEBRATION COMPONENT
# -----------------------------
def get_ariana_profile():
    # Constructing a rich HTML component for Ariana's profile
    # Includes blue and red stars, and celebratory "balloons of encouragement"
    
    html_template = """
    <div style="background-color: #f0f8ff; padding: 20px; border-radius: 15px; text-align: center; border: 4px solid #003366; position: relative;">
        <span style="position: absolute; top: 10px; left: 10px; font-size: 1.5em; color: blue;">💙</span>
        <span style="position: absolute; top: 10px; right: 10px; font-size: 1.5em; color: red;">❤️</span>
        <span style="position: absolute; bottom: 10px; left: 10px; font-size: 1.5em; color: red;">❤️</span>
        <span style="position: absolute; bottom: 10px; right: 10px; font-size: 1.5em; color: blue;">💙</span>
        <span style="position: absolute; top: 50%; left: 5px; font-size: 1.2em; color: blue;">💙</span>
        <span style="position: absolute; top: 50%; right: 5px; font-size: 1.2em; color: red;">❤️</span>

        <div style="width: 200px; height: 200px; border-radius: 50%; border: 5px solid #003366; overflow: hidden; margin: 0 auto 15px auto;">
            <img src="data:image/png;base64,{b64_image}" alt="Ariana" style="width: 100%; height: 100%; object-fit: cover;">
        </div>

        <h2 style="color: #003366; margin-bottom: 5px;">Ariana</h2>
        <p style="color: #ff4500; font-weight: bold; font-size: 1.1em; margin-top: 0;">Our Proud Ambassador 🇭🇹</p>
        <p style="color: #333; font-style: italic; margin-bottom: 15px;">Celebrating courage, joy, and patience representing Haiti in Africa!</p>
        
        <div style="font-size: 2.5em; margin-top: 10px;">
            🎈🎈🎈
        </div>
        
    </div>
    """
    
    # Load and encode the image (assuming it's in the same directory)
    if os.path.exists("Ariana.png"):
        with open("Ariana.png", "rb") as f:
            b64_image = base64.b64encode(f.read()).decode()
        return html_template.format(b64_image=b64_image)
    else:
        # Fallback if image isn't found
        return html_template.format(b64_image="") # Will show a broken image, but keeps the structure

# -----------------------------
# UI LAYOUT
# -----------------------------
left, right = st.columns([3, 1])

with right:
    # 1. Company Logo/Branding (Kept)
    st.markdown("""
        <div style="background-color: #003366; padding: 20px; border-radius: 10px; text-align: center;">
            <h2 style="color: white; margin: 0;">GlobalInternet.py</h2>
            <p style="color: #66ccff; font-size: 0.9em;">Innovation & Tech</p>
        </div>
    """, unsafe_allow_html=True)
    st.markdown("---")
    
    # 2. Ariana Celebration Profile (NEW)
    st.markdown(get_ariana_profile(), unsafe_allow_html=True)
    st.markdown("---")

    # 3. Founder Details (Kept)
    st.markdown("**Builder & Founder:**")
    st.markdown("### Gesner Deslandes")
    st.markdown("📱 (509) 4738-5663")
    st.markdown("📧 deslandes78@gmail.com")
    st.markdown("🔗 [Main Platform](https://globalinternetsitepy-abh7v6tnmskxxnuplrdcgk.streamlit.app/)")
    
    # 4. Haitian Flag (Brought Back to this position)
    st.success("Building the Future 🇭🇹")

with left:
    st.title("🤖 Gesner Humanoid AI")
    # Updated Subheader
    st.subheader("🎉 Honoring Ariana: Our Ambassador to Africa")
    
    language = st.selectbox("🌍 Select Language", list(voices.keys()))
    
    face_placeholder = st.empty()
    face_placeholder.image(create_face(is_open=False))
    
    audio_placeholder = st.empty()

    # Updated Button Text
    if st.button("🚀 Start Celebratory Message"):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
            audio_path = tmp.name
        
        with st.spinner("Generating Celebratory Audio..."):
            asyncio.run(edge_tts.Communicate(texts[language], voices[language]).save(audio_path))
        
        with open(audio_path, "rb") as f:
            audio_bytes = f.read()
            b64 = base64.b64encode(audio_bytes).decode()
        
        # Duration check to sync animation
        duration = MP3(audio_path).info.length
        
        # Audio rendering with controls
        audio_html = f"""
            <audio autoplay="true" controls style="width: 100%;">
                <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
            </audio>
        """
        audio_placeholder.markdown(audio_html, unsafe_allow_html=True)
        
        # --- AGGRESSIVE ANIMATION ENGINE (Kept) ---
        # Forces the mouth to stay in motion for the full duration
        start_time = time.time()
        toggle = True
        
        while (time.time() - start_time) < duration:
            face_placeholder.image(create_face(is_open=toggle))
            toggle = not toggle
            # High-speed toggle for intense promotional look
            time.sleep(0.04) 
        
        # Final reset to closed mouth
        face_placeholder.image(create_face(is_open=False))
        
        if os.path.exists(audio_path):
            os.remove(audio_path)
