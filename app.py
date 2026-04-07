import streamlit as st
from PIL import Image, ImageDraw
import asyncio
import edge_tts
import time

# -----------------------------
# PAGE CONFIG (FIXED LAYOUT FOR SCREEN RECORDING)
# -----------------------------
st.set_page_config(layout="wide")

st.markdown(
    """
    <style>
    .block-container {
        padding-top: 1rem;
        padding-bottom: 0rem;
        max-height: 100vh;
        overflow: hidden;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# -----------------------------
# VOICE SETTINGS
# -----------------------------
voices = {
    "Promo Speech": "en-US-GuyNeural"
}

# -----------------------------
# PROMO SCRIPT (CLEAN DISPLAY VERSION)
# -----------------------------
promo_text = """
GlobalInternet.py – Build with Python. Deliver with Speed.

We don’t just write code. We build complete production-ready software on demand – tailored to your needs, delivered by email in record time.

What we do:
Custom web applications (Streamlit, Flask, Django)
Election & voting systems
AI-powered tools (chatbots, data analysis, automation)
Business dashboards, reporting tools, internal workflows
Any Python-based project you can imagine – we make it work online

Who we are:
GlobalInternet.py was founded by Gesner Deslandes – owner, founder, and lead engineer.
Like Silicon Valley, but with a Haitian touch and outstanding outcomes.
We leverage AI and modern Python frameworks to build fast, reliable, and scalable solutions.

Our promise:
We are an online company working for the world.
No matter where you are, we deliver full software packages via email – ready to install and use.

Contact us:
Phone / WhatsApp: (509)-47385663
Email: deslandes78@gmail.com

GlobalInternet.py – Your Python partner, from Haiti to the world.
"""

# -----------------------------
# SPEECH VERSION (CLEAN TTS)
# -----------------------------
speech_text = """
GlobalInternet py Build with Python Deliver with Speed.

We build complete production ready software on demand tailored to your needs delivered by email in record time.

What we do.
Custom web applications using Streamlit Flask and Django.
Election and voting systems.
Artificial intelligence tools including chatbots data analysis and automation.
Business dashboards reporting tools and internal workflows.
Any Python based project you can imagine we make it work online.

Who we are.
GlobalInternet py was founded by Gesner Deslandes owner founder and lead engineer.
Like Silicon Valley but with a Haitian touch and outstanding results.
We use artificial intelligence and modern Python frameworks to build fast reliable and scalable solutions.

Our promise.
We are an online company working for the world.
We deliver full software packages by email ready to install and use.

Contact us.
Phone or WhatsApp five zero nine four seven three eight five six six three.
Email deslandes78 at gmail dot com.

GlobalInternet py your Python partner from Haiti to the world.
"""

# -----------------------------
# HUMANOID FACE
# -----------------------------
def create_face(mouth_open=False):
    img = Image.new("RGB", (420, 420), "white")
    draw = ImageDraw.Draw(img)

    draw.ellipse((50, 80, 370, 360), outline="black", width=5)
    draw.ellipse((100, 130, 320, 330), outline="black", width=4)

    draw.ellipse((150, 180, 190, 220), fill="black")
    draw.ellipse((230, 180, 270, 220), fill="black")

    if mouth_open:
        draw.ellipse((180, 250, 240, 310), outline="black", width=4)
    else:
        draw.arc((160, 240, 260, 310), start=0, end=180, fill="black", width=4)

    draw.line((210, 90, 210, 50), fill="black", width=4)
    draw.ellipse((195, 30, 225, 60), outline="black", width=3)

    draw.rectangle((40, 190, 70, 270), outline="black", width=3)
    draw.rectangle((350, 190, 380, 270), outline="black", width=3)

    return img

# -----------------------------
# VOICE ENGINE
# -----------------------------
async def generate_voice(text, voice):
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save("voice.mp3")

def estimate_duration(text):
    return len(text.split()) / 2.5

# -----------------------------
# UI LAYOUT (NO SCROLL FIXED VIEW)
# -----------------------------
left, right = st.columns([3, 1])

# RIGHT PANEL (STATIC INFO)
with right:
    st.markdown("### 🏢 GlobalInternet.py")
    st.markdown("Owner: Gesner Deslandes")
    st.markdown("Online Software Company")

    st.markdown("---")
    st.markdown("### 📞 Contact")
    st.markdown("📱 (509)-47385663")
    st.markdown("📧 deslandes78@gmail.com")

    st.markdown("---")
    st.info("Built in Haiti 🇭🇹")

# LEFT PANEL (MAIN)
with left:

    st.title("🤖 Gesner Humanoid AI – GlobalInternet.py Promo")

    st.markdown(
        "<div style='text-align:center;'>"
        "<img src='https://upload.wikimedia.org/wikipedia/commons/5/56/Flag_of_Haiti.svg' width='110'>"
        "</div>",
        unsafe_allow_html=True
    )

    st.markdown("### 📜 GlobalInternet.py Promotional Speech")

    # FIXED BOX (NO SCROLL DURING VIDEO)
    st.text_area("", promo_text, height=320)

    frame = st.empty()
    frame.image(create_face(False))

    if st.button("▶️ Play Promo"):

        asyncio.run(generate_voice(speech_text, voices["Promo Speech"]))

        audio_file = open("voice.mp3", "rb")
        st.audio(audio_file.read(), format="audio/mp3")

        duration = estimate_duration(speech_text)

        start = time.time()
        while time.time() - start < duration:
            frame.image(create_face(True))
            time.sleep(0.2)
            frame.image(create_face(False))
            time.sleep(0.2)

        frame.image(create_face(False))
