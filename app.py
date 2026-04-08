if st.button("▶️ Speak"):

    # Generate voice
    asyncio.run(generate_voice(texts[language], voices[language]))

    audio_file = "voice.mp3"

    # 🔥 AUTO-PLAY AUDIO (NO BUTTON NEEDED)
    import base64
    with open(audio_file, "rb") as f:
        audio_bytes = f.read()
    audio_base64 = base64.b64encode(audio_bytes).decode()

    st.markdown(
        f"""
        <audio autoplay>
        <source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3">
        </audio>
        """,
        unsafe_allow_html=True
    )

    # ✅ REAL AUDIO DURATION
    duration = get_audio_duration(audio_file)

    # 🔥 MOUTH MOVES FULL TIME
    start = time.time()
    mouth = False

    while time.time() - start < duration:
        mouth = not mouth
        frame.image(create_face(mouth))
        time.sleep(0.08)  # smoother animation

    frame.image(create_face(False))
