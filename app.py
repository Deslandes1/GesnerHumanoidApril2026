def create_face(mouth_open=False):
    img = Image.new("RGB", (300, 300), "white")  # smaller but same style
    draw = ImageDraw.Draw(img)

    # Head
    draw.ellipse((30, 60, 270, 270), outline="black", width=4)

    # Inner face
    draw.ellipse((60, 90, 240, 240), outline="black", width=3)

    # Eyes
    draw.ellipse((100, 140, 120, 160), fill="black")
    draw.ellipse((180, 140, 200, 160), fill="black")

    # Mouth animation (same style, just scaled)
    if mouth_open:
        draw.ellipse((120, 190, 180, 240), outline="black", width=3)
    else:
        draw.arc((100, 180, 200, 240), start=0, end=180, fill="black", width=3)

    # Antenna
    draw.line((150, 60, 150, 30), fill="black", width=3)
    draw.ellipse((140, 15, 160, 35), outline="black", width=2)

    # Side panels
    draw.rectangle((20, 150, 40, 220), outline="black", width=2)
    draw.rectangle((260, 150, 280, 220), outline="black", width=2)

    return img
