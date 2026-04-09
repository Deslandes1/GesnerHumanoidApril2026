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
# VOICES & TEXTS (MESSAGE TO MR. WIBY)
# -----------------------------
voices = {
    "English": "en-US-GuyNeural",
    "French": "fr-FR-HenriNeural",
    "Spanish": "es-ES-AlvaroNeural"
}

texts = {
    "English": """Mister Wiby, this is Gesner Deslandes from Be Like Brit. I want to take this moment to tell you: get better soon. 
    The last time I saw you, you had a broken arm in a cast, and I couldn't talk to you since you were heading to the office. 
    Mister Wiby, I know you might not believe it because the Gesner Humanoid AI does not have the voice you are used to hearing, 
    but these are my words and my coding behind this message. I know the members of your church will keep you in their prayers, and so do I. 
    I know you will get better and come back to work as soon as possible at Be Like Brit. 
    Your friend and colleague, Gesner Deslandes, Technology Coordinator at Be Like Brit, Grand Goave, Haiti.""",

    "French": """Monsieur Wiby, c'est Gesner Deslandes de Be Like Brit. Je voulais prendre un moment pour vous dire : bon rétablissement. 
    La dernière fois que je vous ai vu, vous aviez le bras cassé dans le plâtre, et je n'ai pas pu vous parler car vous alliez au bureau. 
    Monsieur Wiby, je sais que vous ne le croirez peut-être pas parce que l'IA Humanoïde Gesner n'a pas la voix que vous avez l'habitude d'entendre, 
    mais ce sont mes mots et mon codage derrière ce message. Je sais que les membres de votre église vous garderont dans leurs prières, et moi aussi. 
    Je sais que vous irez mieux et que vous reviendrez travailler le plus tôt possible à Be Like Brit. 
    Votre ami et collègue, Gesner Deslandes, Coordinateur Technologique à Be Like Brit, Grand Goâve, Haïti.""",

    "Spanish": """Señor Wiby, habla Gesner Deslandes de Be Like Brit. Quiero tomarme este momento para decirte: que te mejores pronto. 
    La última vez que te vi, tenías el brazo roto enyesado y no pude hablar contigo porque ibas a la oficina. 
    Señor Wiby, sé que tal vez no lo creas porque la IA Humanoide de Gesner no tiene la voz que sueles escuchar, 
    pero estas son mis palabras y mi programación detrás de este mensaje. Sé que los miembros de tu iglesia te mantendrán en sus oraciones, al igual que yo. 
    Sé que te recuperarás y volverás al trabajo lo antes posible en Be Like Brit. 
    Tu amigo y colega, Gesner Deslandes, Coordinador de Tecnología en Be Like Brit, Grand Goave, Haití."""
}

# -----------------------------
# FACE DESIGN (AGGRESSIVE BLACK LIPS)
# -----------------------------
def create_face(is_open=False):
    img = Image.new("RGB", (400, 400), "white")
    draw = ImageDraw.Draw(img)

    # Face Shape
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
    st.success("Be Like Brit 🇭🇹")

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

    if st.button("▶️ Play Message for Mr. Wiby"):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
            audio_path = tmp.name

        with st.spinner("Preparing words of kindness..."):
            asyncio.run(edge_tts.Communicate(texts[language], voices[language]).save(audio_path))

        with open(audio_path, "rb") as f:
            b64 = base64.b64encode(f.read()).decode()
        
        duration = MP3(audio_path).info.length
        
        # Audio injection
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
