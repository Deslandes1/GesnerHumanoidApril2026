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
# VOICES & TEXTS (MESSAGE TO THE KIDS)
# -----------------------------
voices = {
    "English": "en-US-GuyNeural",
    "French": "fr-FR-HenriNeural",
    "Spanish": "es-ES-AlvaroNeural"
}

# The personal message from Gesner Deslandes to his sons
texts = {
    "English": """Junior, Roosevelt, and Babas, listen to me. Zendaya is still too small, but you guys are old enough to understand this easily. 
    We make money by creating and selling software through our company, GlobalInternet.py. This company is a legacy for you to take charge of one day. 
    Do not ever break the codes. Instead, study coding to reinforce them, just like your papa Gesner Deslandes, a mastermind, a fighter, and the king of his jungle. 
    Roosevelt, I know you love technology. Junior, I know you love E-football. That is okay, as long as you do your best in active learning and reading. 
    Junior knows how much I value reading. Even if the school doors close, you can use reading to improve your mind and feed your brain. 
    Some call me Tiboul, others call me Mr. G, or even Wakanda Forever. But I will always be your bad ass dad. Gesner Deslandes forever!""",

    "French": """Junior, Roosevelt, et Babas, écoutez-moi. Zendaya est encore trop petite, mais vous êtes assez grands pour comprendre cela facilement. 
    Nous gagnons de l'argent en créant et en vendant des logiciels via notre entreprise, GlobalInternet.py. Cette entreprise est un héritage que vous devrez diriger un jour. 
    Ne cassez jamais les codes. Au lieu de cela, étudiez la programmation pour les renforcer, tout comme votre papa Gesner Deslandes, un cerveau, un combattant et le roi de sa jungle. 
    Roosevelt, je sais que tu aimes la technologie. Junior, je sais que tu aimes l'E-football. C'est bien, tant que vous faites de votre mieux dans l'apprentissage actif et la lecture. 
    Junior sait à quel point j'accorde de l'importance à la lecture. Même si les portes de l'école se ferment, vous pouvez utiliser la lecture pour améliorer votre esprit et nourrir votre cerveau. 
    Certains m'appellent Tiboul, d'autres Mr. G, ou même Wakanda Forever. Mais je serai toujours votre papa dur à cuire. Gesner Deslandes pour toujours !""",

    "Spanish": """Junior, Roosevelt y Babas, escúchenme. Zendaya aún es muy pequeña, pero ustedes tienen la edad suficiente para entender esto fácilmente. 
    Ganamos dinero creando y vendiendo software a través de nuestra empresa, GlobalInternet.py. Esta empresa es un legado para que ustedes se hagan cargo algún día. 
    Nunca rompan los códigos. En su lugar, estudien programación para reforzarlos, al igual que su papá Gesner Deslandes, una mente maestra, un luchador y el rey de su jungla. 
    Roosevelt, sé que te interesa la tecnología. Junior, sé que te interesa el E-football. Eso está bien, siempre y cuando den lo mejor de sí en el aprendizaje activo y la lectura. 
    Junior ya sabe la importancia que le doy a la lectura. Incluso si las puertas de la escuela se cierran, pueden usar la lectura para mejorar su mente y alimentar su cerebro. 
    Algunos me llaman Tiboul, otros Mr. G, o incluso Wakanda Forever. Pero siempre seré su papá rudo. ¡Gesner Deslandes por siempre!"""
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
    st.success("Building a Legacy 🇭🇹")

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

    if st.button("▶️ Play Father's Message"):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
            audio_path = tmp.name

        with st.spinner("Generating father's voice..."):
            asyncio.run(edge_tts.Communicate(texts[language], voices[language]).save(audio_path))

        with open(audio_path, "rb") as f:
            b64 = base64.b64encode(f.read()).decode()
        
        duration = MP3(audio_path).info.length
        
        # Injection and immediate loop start
        st.markdown(f'<audio autoplay><source src="data:audio/mp3;base64,{b64}" type="audio/mp3"></audio>', unsafe_allow_html=True)
        
        start_time = time.time()
        frame_toggle = True

        while (time.time() - start_time) < duration:
            face_frame.image(create_face(is_open=frame_toggle))
            frame_toggle = not frame_toggle
            time.sleep(0.04) 

        face_frame.image(create_face(is_open=False))
        
        if os.path.exists(audio_path):
            os.remove(audio_path)
