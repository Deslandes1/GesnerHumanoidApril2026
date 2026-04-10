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
# VOICES & TEXTS (BUSINESS EDUCATION SCRIPT)
# -----------------------------
voices = {
    "English": "en-US-GuyNeural",
    "French": "fr-FR-HenriNeural",
    "Spanish": "es-ES-AlvaroNeural"
}

texts = {
    "English": """How does a website become a business? It is not just about having a link; it is about solving a problem.
    First, you identify a need, like custom software or educational tools. 
    Second, you build a platform that establishes trust. This is where your branding and professional design come in.
    Third, you implement a monetization model. This could be selling products directly, offering subscription services like our Chess AI, or providing specialized consulting.
    Fourth, you drive traffic. Without people visiting your site, you have no customers. You use social media and quality content to bring people in.
    Finally, you automate and scale. By using Python and Streamlit, we create tools that work for us twenty-four hours a day. 
    At GlobalInternet.py, we don't just build sites; we build engines of commerce. That is how a simple code becomes a professional legacy.""",

    "French": """Comment un site web devient-il une entreprise ? Il ne s'agit pas seulement d'avoir un lien ; il s'agit de résoudre un problème.
    Premièrement, vous identifiez un besoin, comme des logiciels personnalisés ou des outils éducatifs.
    Deuxièmement, vous construisez une plateforme qui établit la confiance. C'est là qu'interviennent votre image de marque et votre design professionnel.
    Troisièmement, vous mettez en œuvre un modèle de monétisation. Il peut s'agir de vendre des produits directement, d'offrir des services d'abonnement comme notre IA d'échecs, ou de fournir des conseils spécialisés.
    Quatrièmement, vous générez du trafic. Sans visiteurs, vous n'avez pas de clients. Vous utilisez les médias sociaux et un contenu de qualité pour attirer les gens.
    Enfin, vous automatisez et passez à l'échelle. En utilisant Python et Streamlit, nous créons des outils qui travaillent pour nous vingt-quatre heures sur vingt-quatre.
    Chez GlobalInternet.py, nous ne construisons pas seulement des sites ; nous construisons des moteurs de commerce.""",

    "Spanish": """¿Cómo se convierte un sitio web en un negocio? No se trata solo de tener un enlace; se trata de resolver un problema.
    Primero, identificas una necesidad, como software personalizado o herramientas educativas.
    Segundo, construyes una plataforma que genere confianza. Aquí es donde entra tu marca y diseño profesional.
    Tercero, implementas un modelo de monetización. Esto podría ser la venta directa de productos, ofrecer servicios de suscripción como nuestra IA de ajedrez, o brindar consultoría especializada.
    Cuarto, generas tráfico. Sin visitas, no hay clientes. Utilizas las redes sociales y contenido de calidad para atraer a la gente.
    Finalmente, automatizas y escalas. Usando Python y Streamlit, creamos herramientas que trabajan para nosotros las veinticuatro horas del día.
    En GlobalInternet.py, no solo construimos sitios; construimos motores de comercio. Así es como un simple código se convierte en un legado profesional."""
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
    st.markdown("## 🌐 GlobalInternet.py")
    st.markdown("**Founder:** Gesner Deslandes")
    st.markdown("📱 (509)-47385663")
    st.markdown("📧 deslandes78@gmail.com")
    st.markdown("🔗 [Main Website](https://globalinternetsitepy-abh7v6tnmskxxnuplrdcgk.streamlit.app/)")
    st.markdown("---")
    st.success("Business Education 🇭🇹")

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

    if st.button("▶️ Start Business Explanation"):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
            audio_path = tmp.name

        with st.spinner("Generating detailed explanation..."):
            asyncio.run(edge_tts.Communicate(texts[language], voices[language]).save(audio_path))

        with open(audio_path, "rb") as f:
            b64 = base64.b64encode(f.read()).decode()
        
        duration = MP3(audio_path).info.length
        
        # Audio injection and instant sync
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
