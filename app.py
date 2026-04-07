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
# FULL SPEECH PER LANGUAGE
# -----------------------------
texts = {
    "English": """GlobalInternet.py – Build with Python. Deliver with Speed.

We don’t just write code. We build complete, production-ready software tailored to your needs and delivered within 24 hours.

Here is how we deliver your software step by step.

After your order is completed, we send you an email containing your full software package.

Inside that email, you will receive a zip file. This zip file contains your app.py file, all required dependencies, and a clear step-by-step guide explaining how to install and run your software.

First, you download the zip file and extract it on your computer or mobile device.

Next, you install the required packages using the provided requirements file.

Then, you simply run the application using Streamlit or Python, following the instructions included in your guide.

You also have the option to upload your project to GitHub and connect it with Streamlit Cloud. This allows you to run your application online and access it from anywhere in the world.

For security, you can store your passwords and private keys safely using Streamlit secret settings.

If you need a professional website or custom software for your business, get in touch with us right now.

We build your solution based on your exact requirements. You tell us what you need, and we handle everything professionally from start to finish.

We can also integrate your company logo or suggest a design that matches your brand identity.

GlobalInternet.py – Your Python partner from Haiti to the world.""",

    "French": """Système de vote en ligne officiel prêt pour les élections en Haïti.
GlobalInternet.py, propriété de Gesner Deslandes...""",

    "Spanish": """Sistema oficial de votación en línea para elecciones en Haití.
Desarrollado por GlobalInternet.py..."""
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
# VOICE GENERATION
# -----------------------------
async def generate_voice(text, voice):
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save("voice.mp3")

# -----------------------------
# REAL AUDIO DURATION
# -----------------------------
def get_audio_duration(file_path):
    audio = MP3(file_path)
    return audio.info.length

# -----------------------------
# UI LAYOUT
# -----------------------------
left, right = st.columns([3, 1])

# RIGHT PANEL
with right:
    st.markdown("### 🏢 Company Info")

    st.markdown("**GlobalInternet.py**")
    st.markdown("Online Software Company")
    st.markdown("Owner: Gesner Deslandes")

    st.markdown("---")
    st.markdown("### 📞 Contact")

    st.markdown("📱 Phone: (509)-47385663")
    st.markdown("📧 Email: deslandes78@gmail.com")
    st.markdown("🏢 Office: Available upon request")

    st.markdown("---")
    st.info("AI & Software Solutions built in Haiti 🇭🇹")

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

        audio_bytes = open(audio_file, "rb").read()
        st.audio(audio_bytes, format="audio/mp3", autoplay=True)

        duration = get_audio_duration(audio_file)

        start = time.time()

        while time.time() - start < duration:
            frame.image(create_face(True))
            time.sleep(0.15)
            frame.image(create_face(False))
            time.sleep(0.15)

        frame.image(create_face(False))
