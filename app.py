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

    "French": """GlobalInternet.py – Construisez avec Python. Livrez avec rapidité.

Nous ne faisons pas que coder. Nous créons des logiciels complets et prêts à l’emploi, adaptés à vos besoins et livrés en moins de 24 heures.

Voici comment nous livrons votre logiciel étape par étape.

Après la finalisation de votre commande, nous vous envoyons un email contenant votre logiciel complet.

Dans cet email, vous recevrez un fichier zip contenant votre fichier app.py, toutes les dépendances nécessaires, ainsi qu’un guide clair expliquant comment installer et exécuter votre logiciel.

D’abord, vous téléchargez le fichier zip et vous l’extrayez sur votre ordinateur ou votre téléphone.

Ensuite, vous installez les dépendances à l’aide du fichier requirements fourni.

Puis, vous lancez simplement l’application avec Streamlit ou Python en suivant le guide.

Vous pouvez aussi utiliser GitHub et Streamlit Cloud pour mettre votre application en ligne et y accéder depuis n’importe où.

Pour la sécurité, vous pouvez enregistrer vos mots de passe en toute sécurité avec les paramètres secrets de Streamlit.

Si vous avez besoin d’un site web ou d’un logiciel professionnel pour votre entreprise, contactez-nous dès maintenant.

Nous construisons votre solution selon vos besoins exacts. Vous expliquez votre projet, et nous faisons le reste de manière professionnelle.

Nous pouvons aussi intégrer le logo de votre entreprise ou vous proposer un design adapté à votre image.

GlobalInternet.py – Votre partenaire Python d’Haïti vers le monde.""",

    "Spanish": """GlobalInternet.py – Construye con Python. Entrega con rapidez.

No solo escribimos código. Creamos software completo y listo para usar, adaptado a tus necesidades y entregado en menos de 24 horas.

Así es como entregamos tu software paso a paso.

Después de completar tu pedido, te enviamos un correo electrónico con tu paquete completo.

Dentro del correo recibirás un archivo zip con tu archivo app.py, todas las dependencias necesarias y una guía clara paso a paso para instalar y ejecutar el software.

Primero, descargas el archivo zip y lo extraes en tu computadora o teléfono.

Luego, instalas las dependencias usando el archivo requirements.

Después, ejecutas la aplicación con Streamlit o Python siguiendo la guía.

También puedes subir tu proyecto a GitHub y conectarlo con Streamlit Cloud para usarlo en línea desde cualquier lugar.

Para mayor seguridad, puedes guardar tus contraseñas usando la configuración secreta de Streamlit.

Si necesitas un sitio web o software profesional para tu negocio, contáctanos ahora mismo.

Construimos tu solución según tus necesidades. Tú nos dices lo que necesitas y nosotros hacemos el resto profesionalmente.

También podemos integrar el logo de tu empresa o sugerir un diseño adecuado para tu marca.

GlobalInternet.py – Tu socio Python desde Haití para el mundo."""
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

with right:
    st.markdown("### 🏢 Company Info")
    st.markdown("**GlobalInternet.py**")
    st.markdown("Owner: Gesner Deslandes")
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
