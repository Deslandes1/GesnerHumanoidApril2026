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
    "English": """Outstanding Determination.

You can make mistakes while trying to do what is right. Not everybody will understand you.

But if you understand yourself, you can start over. You can rebuild and reinstall the best version of yourself.

Not to please people, but to become what you were truly meant to be.

Do not ever let disappointment discourage you or bring you down. Instead, use it as fuel to move forward.

Be unstoppable. Be yourself. Use your mind, and control your mind.

Your inner world is more powerful than your outside world.

People want results. They do not need to know your daily struggles.

Take time for yourself. Love yourself. Forgive yourself.

Move forward with yourself.

Remember: you came into this world alone, and you will leave it alone, with your flaws and your greatness.""",

    "French": """Détermination exceptionnelle.

Vous pouvez faire des erreurs en essayant de faire ce qui est juste. Tout le monde ne vous comprendra pas.

Mais si vous vous comprenez, vous pouvez recommencer et reconstruire la meilleure version de vous-même.

Pas pour plaire aux autres, mais pour devenir ce que vous devez être.

N’ayez pas peur de la déception. Utilisez-la comme carburant pour avancer.

Soyez vous-même. Soyez fort. Contrôlez votre esprit.

Votre monde intérieur est plus puissant que le monde extérieur.

Les gens veulent des résultats, pas vos luttes.

Prenez du temps pour vous. Aimez-vous. Pardonnez-vous.

Avancez.

Rappelez-vous : vous êtes venu seul et vous partirez seul, avec vos défauts et votre grandeur.""",

    "Spanish": """Determinación extraordinaria.

Puedes cometer errores intentando hacer lo correcto. No todos te entenderán.

Pero si te entiendes, puedes empezar de nuevo y reconstruir la mejor versión de ti.

No para agradar a otros, sino para convertirte en quien debes ser.

No dejes que la decepción te detenga. Úsala como combustible.

Sé fuerte. Sé tú mismo. Controla tu mente.

Tu mundo interior es más poderoso que el exterior.

La gente quiere resultados, no tus luchas.

Tómate tiempo. Ámate. Perdónate.

Sigue adelante.

Recuerda: viniste solo y te irás solo, con tus defectos y tu grandeza."""
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
# UI
# -----------------------------
left, right = st.columns([3, 1])

# 🔥 RIGHT PANEL (ENCOURAGEMENT SYMBOL)
with right:
    st.markdown("## 🦁🔥⚡")

    st.markdown("### **OUTSTANDING**")
    st.markdown("### **DETERMINATION**")

    st.markdown("---")

    st.success("Be Strong")
    st.info("Control Your Mind")
    st.warning("Never Give Up")

    st.markdown("---")

    st.markdown("🇭🇹 Built from Haiti to the World")

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
