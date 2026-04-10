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
# VOICES & TEXTS (SENDWAVE SCRIPT)
# -----------------------------
voices = {
    "English": "en-US-GuyNeural",
    "French": "fr-FR-HenriNeural",
    "Spanish": "es-ES-AlvaroNeural"
}

# The educational script for the AI to read
sendwave_script = """Hello, I am the Gesner Humanoid AI. Family is everything, and today, I will explain how your relatives and friends abroad can send support to Haiti instantly using Sendwave. Sendwave is a secure mobile app built for international money transfers with very low fees. Here is how it works: Your family member in the USA, Canada, or Europe downloads the Sendwave app and links their debit card. Then, they simply select Haiti, enter your phone number, and choose how you will receive the funds. They can send the money directly to your Moncash wallet, your Natcash account, or for cash pickup at a trusted local agent. The transfer is completed within seconds, and the money is ready for you to use. It is that simple, fast, and secure. This was Gesner Deslandes, explaining to you how this international money transfer works to keep us connected. Thank you."""

texts = {
    "English": sendwave_script,
    "French": """Bonjour, je suis l'IA Humanoïde Gesner. La famille est tout, et aujourd'hui, j'expliquerai comment vos parents et amis à l'étranger peuvent envoyer un soutien instantané en Haïti en utilisant Sendwave. Sendwave est une application mobile sécurisée pour les transferts d'argent internationaux avec des frais très bas. Voici comment cela fonctionne: votre membre de famille à l'étranger télécharge l'application Sendwave et lie sa carte de débit. Ensuite, ils sélectionnent Haïti, entrent votre numéro de téléphone et choisissent comment vous recevrez les fonds. Ils peuvent envoyer l'argent directement vers votre portefeuille Moncash, votre compte Natcash ou pour un retrait en espèces chez un agent local de confiance. Le transfert est terminé en quelques secondes et l'argent est prêt à être utilisé. C'était Gesner Deslandes, vous expliquant comment fonctionne ce transfert d'argent international pour nous garder connectés. Merci.""",
    "Spanish": """Hola, soy la IA Humanoide de Gesner. La familia lo es todo, y hoy explicaré cómo sus familiares y amigos en el extranjero pueden enviar apoyo instantáneo a Haití usando Sendwave. Sendwave es una aplicación móvil segura para transferencias de dinero internacionales con tarifas muy bajas. Así es como funciona: su familiar en el extranjero descarga la aplicación Sendwave y vincula su tarjeta de débito. Luego, simplemente seleccionan Haití, ingresan su número de teléfono y eligen cómo recibirá los fondos. Pueden enviar el dinero directamente a su billetera Moncash, su cuenta Natcash o para retiro de efectivo en un agente local de confianza. La transferencia se completa en segundos y el dinero está listo para que lo use. Este fue Gesner Deslandes, explicándole cómo funciona esta transferencia internacional de dinero para mantenernos conectados. Gracias."""
}

# -----------------------------
# FACE DESIGN (AGGRESSIVE BLACK LIPS)
# -----------------------------
def create_face(is_open=False):
    img = Image.new("RGB", (400, 400), "white")
    draw = ImageDraw.Draw(img)

    # Face Shape
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
    # SENDWAVE LOGO (MEDIUM SIZE)
    st.image("https://upload.wikimedia.org/wikipedia/commons/e/ea/Sendwave_logo.svg", width=150)
    st.markdown("---")
    st.markdown("## 🌐 GlobalInternet.py")
    st.markdown("**Owner:** Gesner Deslandes")
    st.markdown("📱 (509)-47385663")
    st.markdown("📧 deslandes78@gmail.com")
    st.markdown("🔗 [Main Website](https://globalinternetsitepy-abh7v6tnmskxxnuplrdcgk.streamlit.app/)")
    st.markdown("---")
    st.success("Haiti Global Support 🇭🇹")

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

    if st.button("▶️ Start SendWave presentation"):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
            audio_path = tmp.name

        with st.spinner("Preparing Sendwave presentation..."):
            asyncio.run(edge_tts.Communicate(texts[language], voices[language]).save(audio_path))

        with open(audio_path, "rb") as f:
            b64 = base64.b64encode(f.read()).decode()
        
        duration = MP3(audio_path).info.length
        
        # Audio injection
        st.markdown(f'<audio autoplay><source src="data:audio/mp3;base64,{b64}" type="audio/mp3"></audio>', unsafe_allow_html=True)
        
        start_time = time.time()
        frame_toggle = True

        # THE RELENTLESS ANIMATION LOOP
        while (time.time() - start_time) < duration:
            face_frame.image(create_face(is_open=frame_toggle))
            frame_toggle = not frame_toggle
            time.sleep(0.04) 

        face_frame.image(create_face(is_open=False))
        
        if os.path.exists(audio_path):
            os.remove(audio_path)
