if st.button("▶️ Speak"):

    asyncio.run(generate_voice(texts[language], voices[language]))

    audio_file = "voice.mp3"

    # Convert audio to base64 (autoplay)
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

    # Get REAL audio duration
    duration = get_audio_duration(audio_file)

    # 🔥 FORCE STREAMLIT TO KEEP UPDATING
    start_time = time.time()
    mouth = False

    placeholder = st.empty()

    while time.time() - start_time < duration:
        mouth = not mouth
        placeholder.image(create_face(mouth))
        time.sleep(0.08)  # faster = smoother lips

    placeholder.image(create_face(False))
