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
# VOICES & TEXTS (PAYPAL EXPLAINER)
# -----------------------------
voices = {
    "English": "en-US-GuyNeural",
    "French": "fr-FR-HenriNeural",
    "Spanish": "es-ES-AlvaroNeural"
}

# The educational script for the AI to read
paypal_script = """My name is Gesner Deslandes. Today I want to explain how when you have a PayPal account, you can cash in, cash out, or make any online transaction. 
PayPal works as a digital middleman between your bank and merchants. When you want to pay someone, PayPal securely moves the funds from your linked card or balance to the recipient's email address. 
To get paid, someone simply sends money to your email. These funds sit in your PayPal balance. 
To cash out and put that money in your physical wallet, you must link a local bank account or a debit card. You then select Transfer Funds, and PayPal sends the money to your bank, which usually takes one to three business days. 
In some regions, you can also use a PayPal debit card at an ATM for instant cash. 
Understanding these digital flows is key to running a global business. This was Gesner Deslandes, the owner of GlobalInternet.py."""

texts = {
    "English": paypal_script,
    "French": """Je m'appelle Gesner Deslandes. Aujourd'hui, je veux expliquer comment, lorsque vous avez un compte PayPal, vous pouvez encaisser, retirer ou effectuer toute transaction en ligne. 
    PayPal fonctionne comme un intermédiaire numérique entre votre banque et les marchands. Pour encaisser votre argent dans votre portefeuille réel, vous devez lier un compte bancaire ou une carte. 
    C'était Gesner Deslandes, le propriétaire de GlobalInternet.py.""",
    "Spanish": """Mi nombre es Gesner Deslandes. Hoy quiero explicar cómo, cuando tienes una cuenta de PayPal, puedes ingresar, retirar o realizar cualquier transacción en línea. 
    PayPal funciona como un intermediario digital entre su banco y los comerciantes. Para retirar su dinero a su billetera real, debe vincular una cuenta bancaria o tarjeta. 
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
        draw.ellipse((140, center_y - 35, 260, center_y + 35), fill="black")
    else:
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
    # PAYPAL SYMBOL ADDED
    st.image("https://upload.wikimedia.org/wikipedia/commons/b/b5/PayPal.svg", width=100)
    st.markdown("## 🌐 GlobalInternet.py")
    st.markdown("**Owner:** Gesner Deslandes")
    st.markdown("📱 (509)-47385663")
    st.markdown("📧 deslandes78@gmail.com")
    st.markdown("🔗 [Main Website](https://globalinternetsitepy-abh7v6tnmskxxnuplrdcgk.streamlit.app/)")
    st.markdown("---")
    st.success("Fintech & Software 🇭🇹")

with left:
    st.title("🤖 Gesner Humanoid AI")
    
    # THE HAITIAN FLAG
    st.markdown(
        "<div style='text-align:center;'><img src='https://upload.wikimedia.org/wikipedia/commons/5/56/Flag_of_Haiti.svg' width='120'></div>",
        unsafe_allow_html=True
    )
    
    language = st.selectbox("🌍 Select Language", list(voices.keys()))
    
    # Teleprompter view
    st.info("AI Explainer: Digital Transactions & PayPal")
    
    face_frame = st.empty()
    face_frame.image(create_face(is_open=False))

    if st.button("▶️ Start PayPal Explanation"):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
            audio_path = tmp.name

        with st.spinner("Gesner AI is calculating transaction logic..."):
            asyncio.run(edge_tts.Communicate(texts[language], voices[language]).save(audio_path))

        with open(audio_path, "rb") as f:
            b64 = base64.b64encode(f.read()).decode()
        
        duration = MP3(audio_path).info.length
        
        # Immediate audio injection
        st.markdown(f'<audio autoplay><source src="data:audio/mp3;base64,{b64}" type="audio/mp3"></audio>', unsafe_allow_html=True)
        
        start_time = time.time()
        frame_toggle = True

        # AGGRESSIVE ANIMATION LOOP SYNCED TO AUDIO
        while (time.time() - start_time) < duration:
            face_frame.image(create_face(is_open=frame_toggle))
            frame_toggle = not frame_toggle
            time.sleep(0.04) 

        face_frame.image(create_face(is_open=False))
        
        if os.path.exists(audio_path):
            os.remove(audio_path)
