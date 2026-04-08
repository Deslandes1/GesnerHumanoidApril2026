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
# MOTIVATION SPEECH
# -----------------------------
texts = {
    "English": """Outstanding Determination...
You can make mistakes while trying to do what is right...
But if you understand yourself, you can start over...
Rebuild the best version of yourself...
Do not let disappointment stop you...
Use it as fuel...
Be unstoppable. Be yourself. Control your mind...
Your inner world is more powerful than your outside world...
Take time for yourself. Love yourself. Forgive yourself...
Move forward...
You came alone, you leave alone, with your greatness.""",

    "French": """Détermination exceptionnelle...
Vous pouvez faire des erreurs...
Mais vous pouvez recommencer...
Reconstruire votre meilleure version...
Utilisez la déception comme carburant...
Soyez fort, contrôlez votre esprit...
Votre monde intérieur est puissant...
Aimez-vous, pardonnez-vous...
Avancez toujours...""",

    "Spanish": """Determinación extraordinaria...
Puedes cometer errores...
Pero puedes empezar de nuevo...
Reconstruir tu mejor versión...
Usa la decepción como combustible...
Sé fuerte, controla tu mente...
Tu mundo interior es poderoso...
Ámate, perdónate...
Sigue adelante..."""
}

# -----------------------------
# FACE
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
# UI
# -----------------------------
left, right = st.columns([3, 1])

# RIGHT PANEL (SYMBOL)
with right:
    st.markdown("## 🦁🔥⚡")
    st.markdown("### OUTSTANDING")
    st.markdown("### DETERMINATION")
    st.success("Never Give Up")

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

        # Generate voice
        asyncio.run(generate_voice(texts[language], voices[language]))

        audio_file = "voice.mp3"

        # Get REAL duration
        duration = get_audio_duration(audio_file)

        # Play audio
        st.audio(open(audio_file, "rb").read(), autoplay=True)

        # 🔥 PERFECT LIP SYNC LOOP
        start_time = time.time()
        mouth_open = False

        while True:
            elapsed = time.time() - start_time

            if elapsed >= duration:
                break

            mouth_open = not mouth_open
            frame.image(create_face(mouth_open))

            # Faster animation = more realistic
            time.sleep(0.12)

        # End state
        frame.image(create_face(False))
