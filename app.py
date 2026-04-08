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

Be unstoppable. Be yourself. Use your mind, and most importantly, control your mind.

Your inner world is more powerful than your outside world.

People want to see results. They do not need to know your daily struggles.

So take time for yourself. Love yourself. Forgive yourself.

And move forward with yourself.

Because remember this: you came into this world alone, and you will leave it alone, with all your flaws and all your greatness.""",

    "French": """Détermination exceptionnelle.

Vous pouvez faire des erreurs en essayant de faire ce qui est juste. Tout le monde ne vous comprendra pas.

Mais si vous vous comprenez vous-même, vous pouvez recommencer. Vous pouvez reconstruire la meilleure version de vous-même.

Non pas pour plaire aux autres, mais pour devenir ce que vous êtes réellement destiné à être.

Ne laissez jamais la déception vous décourager ou vous abattre. Utilisez-la comme un carburant pour avancer.

Soyez inarrêtable. Soyez vous-même. Utilisez votre esprit et surtout contrôlez-le.

Votre monde intérieur est plus puissant que votre monde extérieur.

Les gens veulent voir les résultats. Ils n’ont pas besoin de connaître vos luttes quotidiennes.

Prenez du temps pour vous. Aimez-vous. Pardonnez-vous.

Et avancez avec vous-même.

Rappelez-vous ceci : vous êtes venu seul dans ce monde, et vous en repartirez seul, avec vos défauts et votre grandeur.""",

    "Spanish": """Determinación extraordinaria.

Puedes cometer errores al intentar hacer lo correcto. No todos te van a entender.

Pero si tú te entiendes a ti mismo, puedes comenzar de nuevo. Puedes reconstruir la mejor versión de ti.

No para complacer a otros, sino para convertirte en lo que realmente estás destinado a ser.

No dejes que la decepción te desanime ni te derribe. Úsala como combustible para seguir adelante.

Sé imparable. Sé tú mismo. Usa tu mente y, sobre todo, contrólala.

Tu mundo interior es más poderoso que tu mundo exterior.

La gente quiere ver resultados. No necesitan conocer tus luchas diarias.

Tómate tiempo para ti. Ámate. Perdónate.

Y sigue avanzando contigo mismo.

Recuerda esto: viniste solo a este mundo y te irás solo, con tus defectos y tu grandeza."""
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

with right:
    st.markdown("### 🏢 GlobalInternet.py")
    st.markdown("Gesner Deslandes")
    st.markdown("📱 (509)-47385663")
    st.markdown("📧 deslandes78@gmail.com")

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
