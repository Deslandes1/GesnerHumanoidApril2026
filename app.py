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
# VOICES & BUSINESS MISSION SCRIPT
# -----------------------------
voices = {
    "English": "en-US-GuyNeural",
    "French": "fr-FR-HenriNeural"
}

mission_script_en = """
Hello, this is Gesner Deslandes, the owner and founder of GlobalInternet.py. 
Today I want to tell our audience that our company is a business one. 
When we display our flag on the software we have built, that is to showcase our origin and add more value to our company and products, to show to the world where we are from. 
However, we are an online company operating in the cloud. 
I myself, Gesner Deslandes, I am a businessman and I build to innovate and sell, nothing more, nothing less. 
I build, I don't talk much, that is what I do in my company every single day. 
Having fun building software for sale, it is all about business and innovation. 
We also look for new partnerships to work together to innovate together. 
Knowledge has no limits. However, we build wealthy and healthy for our community and for the world. 
That was Gesner Deslandes, the Owner of GlobalInternet.py.
"""

mission_script_fr = """
Bonjour, c'est Gesner Deslandes, propriétaire et fondateur de GlobalInternet.py. 
Aujourd'hui, je veux dire à notre public que notre entreprise est une affaire commerciale. 
Lorsque nous affichons notre drapeau sur les logiciels que nous avons créés, c'est pour montrer notre origine et ajouter de la valeur à notre entreprise et à nos produits, pour montrer au monde d'où nous venons. 
Cependant, nous sommes une entreprise en ligne opérant dans le cloud. 
Moi-même, Gesner Deslandes, je suis un homme d'affaires et je construis pour innover et vendre, rien de plus, rien de moins. 
Je construis, je ne parle pas beaucoup, c'est ce que je fais dans mon entreprise chaque jour. 
S'amuser à créer des logiciels pour la vente, tout est question de business et d'innovation. 
Nous recherchons également de nouveaux partenariats pour travailler ensemble et innover ensemble. 
La connaissance n'a pas de limites. Cependant, nous construisons de manière prospère et saine pour notre communauté et pour le monde. 
C'était Gesner Deslandes, le propriétaire de GlobalInternet.py.
"""

texts = {
    "English": mission_script_en,
    "French": mission_script_fr
}

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
        draw.ellipse((130, center_y - 40, 270, center_y + 40), fill="black")
    else:
        draw.line((150, center_y, 250, center_y), fill="black", width=15)
        
    draw.line((200, 40, 200, 80), fill="black", width=4)
    draw.ellipse((185, 20, 215, 50), outline="black", width=3)
    return img

# -----------------------------
# UI LAYOUT
# -----------------------------
left, right = st.columns([3, 1])

with right:
    st.markdown("""
        <div style="background-color: #003366; padding: 20px; border-radius: 10px; text-align: center;">
            <h2 style="color: white; margin: 0;">GlobalInternet.py</h2>
            <p style="color: #66ccff; font-size: 0.9em;">Fast Software Solutions</p>
        </div>
    """, unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("**Builder & Founder:**")
    st.markdown("### Gesner Deslandes")
    st.markdown("📱 (509) 4738-5663")
    st.markdown("📧 deslandes78@gmail.com")
    st.markdown("🔗 [Portfolio](https://globalinternetsitepy-abh7v6tnmskxxnuplrdcgk.streamlit.app/)")
    st.success("Business & Innovation 📈")

with left:
    st.title("🤖 Gesner Humanoid AI")
    st.subheader("Official Founder's Statement")
    
    st.markdown("<div style='text-align:center;'><img src='https://upload.wikimedia.org/wikipedia/commons/5/56/Flag_of_Haiti.svg' width='100'></div>", unsafe_allow_html=True)
    
    language = st.selectbox("🌍 Select Language", list(voices.keys()))
    
    face_placeholder = st.empty()
    face_placeholder.image(create_face(is_open=False))
    
    audio_placeholder = st.empty()

    if st.button("▶️ Generate and Play Audio"):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
            audio_path = tmp.name
        
        with st.spinner("Generating Speech..."):
            asyncio.run(edge_tts.Communicate(texts[language], voices[language]).save(audio_path))
        
        with open(audio_path, "rb") as f:
            audio_bytes = f.read()
            b64 = base64.b64encode(audio_bytes).decode()
        
        duration = MP3(audio_path).info.length
        
        # We place the audio tag in the placeholder first to trigger playback
        audio_html = f"""
            <audio autoplay="true" controls>
                <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
                Your browser does not support the audio element.
            </audio>
        """
        audio_placeholder.markdown(audio_html, unsafe_allow_html=True)
        
        # CONTINUOUS AGGRESSIVE ANIMATION LOOP
        start_time = time.time()
        toggle = True
        while (time.time() - start_time) < duration:
            face_placeholder.image(create_face(is_open=toggle))
            toggle = not toggle
            time.sleep(0.04) 
        
        face_placeholder.image(create_face(is_open=False))
        
        if os.path.exists(audio_path):
            os.remove(audio_path)
