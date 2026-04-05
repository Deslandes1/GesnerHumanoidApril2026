import streamlit as st
from PIL import Image, ImageDraw

def create_robot_face():
    img = Image.new("RGB", (400, 400), "white")
    draw = ImageDraw.Draw(img)

    draw.ellipse((50, 50, 350, 350), outline="black", width=5)
    draw.ellipse((140, 150, 180, 190), fill="black")
    draw.ellipse((220, 150, 260, 190), fill="black")
    draw.arc((150, 200, 250, 300), start=0, end=180, fill="black", width=4)

    draw.line((200, 50, 200, 20), fill="black", width=4)
    draw.ellipse((190, 5, 210, 25), outline="black", width=3)

    return img

st.title("🤖 Gesner Humanoid AI")

robot = create_robot_face()
st.image(robot)

if st.button("Speak"):
    st.markdown("""
    <script>
    var msg = new SpeechSynthesisUtterance(
    "Hello World, this is Gesner Deslandes. I build software now. My company GlobalInternet.py is heading to humanoid projects, please stay tuned!"
    );
    msg.lang = "en-US";
    msg.pitch = 1;
    msg.rate = 0.9;
    speechSynthesis.speak(msg);
    </script>
    """, unsafe_allow_html=True)
