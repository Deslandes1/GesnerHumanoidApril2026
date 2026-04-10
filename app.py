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
# VOICES & TEXTS (PAYPAL SCRIPT)
# -----------------------------
voices = {
    "English": "en-US-GuyNeural",
    "French": "fr-FR-HenriNeural",
    "Spanish": "es-ES-AlvaroNeural"
}

# The educational script for the AI to read
paypal_script = """My name is Gesner Deslandes. Today I want to explain how when you have a PayPal account, you can cash in, cash out, or make any online transaction. 
PayPal works as a digital wallet that connects your bank account or credit card to the internet. 
When you pay someone, PayPal acts as a secure shield so the merchant never sees your bank details. 
To get paid, your email address is all you need. Once the money is in your PayPal balance, you can cash it out by transferring it to your linked bank account or debit card. 
The money moves from the digital world into your physical wallet in just a few days. 
This is the power of fintech for global business. This was Gesner Deslandes, the owner of GlobalInternet.py."""

texts = {
    "English": paypal_script,
    "French": """Je m'appelle Gesner Deslandes. Aujourd'hui, je veux vous expliquer comment utiliser PayPal pour vos transactions. 
    PayPal est un portefeuille numérique sécurisé. Vous pouvez recevoir de l'argent via votre e-mail et le transférer vers votre compte bancaire pour le retirer en espèces. 
    C'était Gesner Deslandes, le propriétaire de GlobalInternet.py.""",
    "Spanish": """Mi nombre es Gesner Deslandes. Hoy quiero explicarles cómo funciona PayPal. 
    Es una billetera digital que protege sus datos. Puede recibir pagos con su correo electrónico y transferir ese dinero a su banco para tener efectivo. 
    Este fue Gesner Deslandes, el dueño de GlobalInternet.py."""
}

# -----------------------------
# FACE DESIGN (AGGRESSIVE BLACK LIPS)
# -----------------------------
def create_face(is_open=False):
    img = Image.new("RGB", (400, 400), "white")
    draw = ImageDraw.Draw(img)

    # Face Outlines
    draw.ellipse((50, 80, 350, 350), outline="black", width=5)
    draw.ellipse((90, 120, 310, 320), outline="black", width=3)
    
    # Eyes
    draw.ellipse((140, 170, 180, 210), fill="black")
    draw.ellipse((220, 170, 260, 210), fill="black")

    # --- AGGRESSIVE BLACK MOUTH ---
    center_y = 265
    if is_open:
        # High-visibility open state
        draw.ellipse((140, center_y - 35, 260, center_y + 35), fill="black")
    else:
        # Heavy closed state
        draw.line((150, center_y, 250, center_y), fill="black", width=12)

    # Robot Details
    draw.line((200, 80, 200, 40), fill="black", width=4)
    draw.ellipse((185, 20, 215, 50), outline="black", width=3)
    draw.rectangle((40, 180, 70, 260), outline="black", width=3)
    draw.rectangle((330, 180, 360, 260), outline="black", width=3)

    return img

# -----------------------------
# LOGIC & UI
# -----------------------------
left, right = st.columns([3, 1])

with right:
    # PAYPAL COLOR LOGIC (MEDIUM SIZE)
    st.image("https://upload.wikimedia.org/wikipedia/commons/b/b5/PayPal.svg", width=150)
    st.markdown("---")
    st.markdown("## 🌐 GlobalInternet.py")
    st.markdown("**Owner:** Gesner Deslandes")
    st.markdown("📱 (509)-47385663")
    st.markdown("📧 deslandes78@gmail.com")
    st.markdown("🔗 [Main Website](https://globalinternetsitepy-abh7v6tnmskxxnuplrdcgk.streamlit.app/)")
    st.markdown("---")
    st.success("Software Solutions 🇭🇹")

with left:
    st.title("🤖 Gesner Humanoid AI")
    
    # THE HAITIAN FLAG
    st.markdown(
        "<div style='text-align:center;'><img src='https://upload.wikimedia.org/wikipedia/commons/5/56/Flag_of_Haiti.svg' width='120'></div>",
        unsafe_allow_html=True
    )
    
    language = st.selectbox("🌍 Select Language", list(voices.keys()))
    
    face_frame = st.empty()
    face_frame.image(create_face(is_open=False))

    if st.button("▶️ Start PayPal Presentation"):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
            audio_path = tmp.name

        with st.spinner("Preparing speech..."):
            asyncio.run(edge_tts.Communicate(texts[language], voices[language]).save(audio_path))

        with open(audio_path, "rb") as f:
            b64 = base64.b64encode(f.read()).decode()
        
        duration = MP3(audio_path).info.length
        
        # Audio injection
        st.markdown(f'<audio autoplay><source src="data:audio/mp3;base64,{b64}" type="audio/mp3"></audio>', unsafe_allow_html=True)
        
        start_time = time.time()
        frame_toggle = True

        # THE AGGRESSIVE ANIMATION LOOP
        while (time.time() - start_time) < duration:
            face_frame.image(create_face(is_open=frame_toggle))
            frame_toggle = not frame_toggle
            time.sleep(0.04) 

        # Return to closed state
        face_frame.image(create_face(is_open=False))
        
        if os.path.exists(audio_path):
            os.remove(audio_path)
