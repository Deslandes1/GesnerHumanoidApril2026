import streamlit as st
from PIL import Image, ImageDraw
import asyncio
import edge_tts
import time
from mutagen.mp3 import MP3

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(layout="wide")

# -----------------------------
# VOICE SETTINGS
# -----------------------------
voices = {
    "English": "en-US-GuyNeural",
    "French": "fr-FR-HenriNeural",
    "Spanish": "es-ES-AlvaroNeural"
}

# -----------------------------
# WEBSITE PROMO SPEECH
# -----------------------------
texts = {

    "English": """Discover GlobalInternet.py – Your Python Software Partner.

We just launched our official company website, and it is now fully multilingual in Haitian Creole, French, English, and Spanish.

Here is what you will find on the site.

About us – founded by Gesner Deslandes, building Python software on demand.

Our services – artificial intelligence, election systems, dashboards, web applications, and 24 hour delivery.

Projects for sale – complete software packages including Haiti Voting System, Business Dashboard, AI Chatbot, School Management System, Point of Sale, and Web Scraper.

Support us – you can donate easily using Moncash with Prisme transfer, up to one hundred thousand Haitian gourdes.

Contact – phone, WhatsApp, and email. We deliver full software code by email.

Visit now:
globalinternetsitepy dash abh7v6tnmskxxnuplrdcgk dot streamlit dot app.

Proudly Haitian, serving the world with Python and artificial intelligence.""",

    "French": """Découvrez GlobalInternet.py – votre partenaire logiciel Python.

Nous venons de lancer notre site officiel, désormais disponible en créole haïtien, français, anglais et espagnol.

Voici ce que vous trouverez sur le site.

À propos – fondé par Gesner Deslandes, créant des logiciels Python à la demande.

Nos services – intelligence artificielle, systèmes électoraux, tableaux de bord, applications web et livraison en 24 heures.

Projets à vendre – solutions complètes incluant système de vote haïtien, tableau de bord, chatbot IA, gestion scolaire, point de vente et extraction de données web.

Soutenez-nous – vous pouvez faire un don facilement via Moncash avec transfert Prisme jusqu’à cent mille gourdes.

Contact – téléphone, WhatsApp et email. Nous livrons le code complet par email.

Visitez maintenant:
globalinternetsitepy tiret abh7v6tnmskxxnuplrdcgk point streamlit point app.

Fièrement haïtien, au service du monde avec Python et l’intelligence artificielle.""",

    "Spanish": """Descubre GlobalInternet.py – tu socio en software Python.

Acabamos de lanzar nuestro sitio web oficial, ahora disponible en criollo haitiano, francés, inglés y español.

Esto es lo que encontrarás en el sitio.

Sobre nosotros – fundado por Gesner Deslandes, desarrollando software en Python a pedido.

Nuestros servicios – inteligencia artificial, sistemas electorales, paneles, aplicaciones web y entrega en 24 horas.

Proyectos en venta – paquetes completos incluyendo sistema de votación de Haití, panel empresarial, chatbot de IA, gestión escolar, punto de venta y web scraper.

Apóyanos – puedes donar fácilmente usando Moncash con transferencia Prisme hasta cien mil gourdes haitianos.

Contacto – teléfono, WhatsApp y correo electrónico. Entregamos el código completo por email.

Visita ahora:
globalinternetsitepy guion abh7v6tnmskxxnuplrdcgk punto streamlit punto app.

Orgullosamente haitiano, sirviendo al mundo con Python e inteligencia artificial."""
}

# -----------------------------
# HUMANOID FACE
# -----------------------------
def create_face(mouth_open=False):
    img = Image.new("RGB", (400, 400), "white")
    draw = ImageDraw.Draw(img)

    draw.ellipse((50, 80, 350, 350), outline="black", width=5)
    draw.ellipse((90, 120, 310, 320), outline="black", width=4)

    draw.ellipse((140, 170, 180, 210), fill="black")
    draw.ellipse((220, 170, 260, 210), fill="black")

    if mouth_open:
        draw.ellipse((170, 240, 230, 300), outline="black", width=4)
    else:
        draw.arc((150, 230, 250, 300), start=0, end=180, fill="black", width=4)

    draw.line((200, 80, 200, 40), fill="black", width=4)
    draw.ellipse((185, 20, 215, 50), outline="black", width=3)

    draw.rectangle((40, 180, 70, 260), outline="black", width=3)
    draw.rectangle((330, 180, 360, 260), outline="black", width=3)

    return img

# -----------------------------
# VOICE
# -----------------------------
async def generate_voice(text, voice):
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save("voice.mp3")

def get_audio_duration(file_path):
    return MP3(file_path).info.length

# -----------------------------
# UI LAYOUT
# -----------------------------
left, right = st.columns([3, 1])

# RIGHT PANEL
with right:
    st.markdown("### 🏢 Company Info")
    st.markdown("**GlobalInternet.py**")
    st.markdown("Owner: Gesner Deslandes")
    st.markdown("📱 (509)-47385663")
    st.markdown("📧 deslandes78@gmail.com")
    st.markdown("---")
    st.success("AI & Software Solutions 🇭🇹")

# LEFT PANEL
with left:

    st.title("🤖 Gesner Humanoid AI")

    st.markdown(
        "<div style='text-align:center;'><img src='https://upload.wikimedia.org/wikipedia/commons/5/56/Flag_of_Haiti.svg' width='120'></div>",
        unsafe_allow_html=True
    )

    language = st.selectbox("🌍 Select Language", list(voices.keys()))

    frame = st.empty()
    frame.image(create_face(False))

    if st.button("▶️ Speak"):

        asyncio.run(generate_voice(texts[language], voices[language]))

        audio_file = "voice.mp3"
        st.audio(open(audio_file, "rb").read(), autoplay=True)

        duration = get_audio_duration(audio_file)
        start = time.time()

        while time.time() - start < duration:
            frame.image(create_face(True))
            time.sleep(0.15)
            frame.image(create_face(False))
            time.sleep(0.15)

        frame.image(create_face(False))
