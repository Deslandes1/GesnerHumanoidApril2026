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
# VOICES & TEXTS (SCRIPT UPDATED)
# -----------------------------
voices = {
    "English": "en-US-GuyNeural",
    "French": "fr-FR-HenriNeural",
    "Spanish": "es-ES-AlvaroNeural"
}

# The message you provided is now the core script for the AI
texts = {
    "English": """Gesner Deslandes – GlobalInternet.py. 
Building Python software from Haiti to the world. 
I invite you to visit our newly improved website. Here’s what you’ll see and notice: 
A professional, multilingual site in English, French, Spanish, and Kreyòl. 
My full background as a Python developer, technology coordinator, interpreter, and more. 
A clear list of services including custom development, AI, dashboards, and 24 hour delivery. 
Ten completed software projects, each with price, status, and Request Info. 
Live demos where you can instantly try the Haiti Voting Software, Accountant Excel AI, and DSM-2026 Radar. The password is 20082010. 
Easy donation to support us via Moncash Prisme transfer. 
Direct contact via phone, email, and a clear call to action. 
No more broken demos. No more confusion. Just working software, proudly made in Haiti. 
Visit now at global internet site p y. 
Your feedback is welcome. Let’s build the future together.""",

    "French": """Gesner Deslandes – GlobalInternet.py. 
Développement de logiciels Python d'Haïti vers le monde. 
Je vous invite à visiter notre site Web nouvellement amélioré. Voici ce que vous verrez : 
Un site professionnel et multilingue en anglais, français, espagnol et kreyòl. 
Mon parcours complet en tant que développeur Python, coordinateur technologique, interprète, et plus encore. 
Une liste claire de services incluant le développement personnalisé, l'IA, les tableaux de bord et la livraison en 24 heures. 
Dix projets logiciels terminés, chacun avec prix, statut et demande d'informations. 
Des démos en direct où vous pouvez essayer instantanément le logiciel de vote en Haïti, l'IA Accountant Excel et le radar DSM-2026. Le mot de passe est 20082010. 
Don facile pour nous soutenir via le transfert Moncash Prisme. 
Contact direct par téléphone, e-mail et un appel à l'action clair. 
Plus de démos cassées. Plus de confusion. Juste des logiciels fonctionnels, fièrement fabriqués en Haïti. 
Visitez maintenant sur global internet site p y. 
Vos commentaires sont les bienvenus. Construisons l'avenir ensemble.""",

    "Spanish": """Gesner Deslandes – GlobalInternet.py. 
Construyendo software Python desde Haití para el mundo. 
Los invito a visitar nuestro sitio web recientemente mejorado. Esto es lo que verán y notarán: 
Un sitio profesional y multilingüe en inglés, francés, español y kreyòl. 
Mi trayectoria completa como desarrollador Python, coordinador de tecnología, intérprete y más. 
Una lista clara de servicios que incluye desarrollo personalizado, IA, tableros de control y entrega en 24 horas. 
Diez proyectos de software completados, cada uno con precio, estado y solicitud de información. 
Demos en vivo donde pueden probar instantáneamente el Software de Votación de Haití, Accountant Excel AI y DSM-2026 Radar. La contraseña es 20082010. 
Donación fácil para apoyarnos a través de la transferencia Moncash Prisme. 
Contacto directo por teléfono, correo electrónico y un claro llamado a la acción. 
No más demos rotos. No más confusión. Solo software que funciona, hecho con orgullo en Haití. 
Visite ahora en global internet site p y. 
Sus comentarios son bienvenidos. Construyamos el futuro juntos."""
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
        # Huge black opening
        draw.ellipse((140, center_y - 35, 260, center_y + 35), fill="black")
    else:
        # Thick closed black line
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
    st.markdown("**Owner:** Gesner Deslandes")
    st.markdown("📱 (509)-47385663")
    st.markdown("📧 deslandes78@gmail.com")
    st.markdown("🔗 [Main Website](https://globalinternetsitepy-abh7v6tnmskxxnuplrdcgk.streamlit.app/)")
    st.markdown("---")
    st.success("AI & Software Solutions 🇭🇹")

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

    if st.button("▶️ Start Announcement"):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
            audio_path = tmp.name

        with st.spinner("Gesner AI is preparing the announcement..."):
            asyncio.run(edge_tts.Communicate(texts[language], voices[language]).save(audio_path))

        # Play Audio
        with open(audio_path, "rb") as f:
            b64 = base64.b64encode(f.read()).decode()
            st.markdown(f'<audio autoplay><source src="data:audio/mp3;base64,{b64}" type="audio/mp3"></audio>', unsafe_allow_html=True)

        # Precise Duration
        duration = MP3(audio_path).info.length
        start_time = time.time()

        # --- THE RELENTLESS ANIMATION LOOP ---
        frame_toggle = True
        while (time.time() - start_time) < duration:
            face_frame.image(create_face(is_open=frame_toggle))
            frame_toggle = not frame_toggle
            time.sleep(0.04) 

        # Final Close
        face_frame.image(create_face(is_open=False))
        
        if os.path.exists(audio_path):
            os.remove(audio_path)
