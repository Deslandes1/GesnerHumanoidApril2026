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
# PERSONAL MESSAGE (ALL LANGUAGES)
# -----------------------------
texts = {

    "English": """Junior, my firstborn, now you must replace my presence to protect and guide your little brothers and your only sister.

We must teach ourselves how to use artificial intelligence in the right way.

As I told you, Junior, I will do my best to send you to school next year. With God's help, you will learn English and computing so you can prepare to work with me in our company, GlobalInternet.py.

Together, we will build software for the world, not only in Haiti.

I, your father, Gesner Deslandes, am a living warrior who is about to conquer economic independence.

My symbol is the lion, strong and fearless. I am a real fighter, and I will never lose any fight.

Roosevelt, Babas, and Zendaya, I think about you every single day. I want to make your lives better and happy.

We will do this together. And as I always say, I will never give up on you.

I am a special dad. I am the father I never had.

Do not be afraid of anything. Instead, let everything be afraid of you, because you are my children, growing strong in Meriken City, Port-au-Prince.

You must start to be proud of me, proud of yourselves, and proud of our future.

Your dad, Gesner Deslandes, the lion heart.""",

    "French": """Junior, mon premier fils, tu dois maintenant remplacer ma présence pour protéger et guider tes petits frères et ta seule sœur.

Nous devons apprendre à utiliser l’intelligence artificielle de la bonne manière.

Comme je te l’ai dit, Junior, je ferai de mon mieux pour t’envoyer à l’école l’année prochaine. Avec l’aide de Dieu, tu apprendras l’anglais et l’informatique pour te préparer à travailler avec moi dans notre entreprise GlobalInternet.py.

Ensemble, nous construirons des logiciels pour le monde, pas seulement pour Haïti.

Moi, ton père Gesner Deslandes, je suis un combattant vivant prêt à atteindre l’indépendance économique.

Mon symbole est le lion, fort et courageux. Je suis un vrai combattant et je ne perdrai jamais aucun combat.

Roosevelt, Babas et Zendaya, je pense à vous chaque jour pour améliorer votre vie et vous rendre heureux.

Nous allons le faire ensemble. Et comme je le dis toujours, je n’abandonnerai jamais.

Je suis un père spécial. Je suis le père que je n’ai jamais eu.

N’ayez peur de rien. Au contraire, que tout ait peur de vous, car vous êtes mes enfants, grandissant à Meriken City, Port-au-Prince.

Soyez fiers de moi, fiers de vous-mêmes et fiers de notre avenir.

Votre père, Gesner Deslandes, au cœur de lion.""",

    "Spanish": """Junior, mi hijo mayor, ahora debes reemplazar mi presencia para proteger y guiar a tus hermanos menores y a tu única hermana.

Debemos aprender a usar la inteligencia artificial de la manera correcta.

Como te dije, Junior, haré todo lo posible para enviarte a la escuela el próximo año. Con la ayuda de Dios, aprenderás inglés e informática para prepararte y trabajar conmigo en nuestra empresa GlobalInternet.py.

Juntos construiremos software para el mundo, no solo para Haití.

Yo, tu padre Gesner Deslandes, soy un luchador que está a punto de conquistar la independencia económica.

Mi símbolo es el león, fuerte y valiente. Soy un verdadero luchador y nunca perderé ninguna batalla.

Roosevelt, Babas y Zendaya, pienso en ustedes todos los días para hacer sus vidas mejores y más felices.

Lo haremos juntos. Y como siempre digo, nunca me rendiré con ustedes.

Soy un padre especial. Soy el padre que nunca tuve.

No tengan miedo de nada. Al contrario, que todo tenga miedo de ustedes, porque son mis hijos creciendo fuertes en Meriken City, Puerto Príncipe.

Deben sentirse orgullosos de mí, orgullosos de ustedes mismos y orgullosos de nuestro futuro.

Su padre, Gesner Deslandes, corazón de león."""
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
