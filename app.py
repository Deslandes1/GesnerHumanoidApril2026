def create_face(mouth_open=False):
    img = Image.new("RGB", (400, 400), "white")
    draw = ImageDraw.Draw(img)

    brown = (120, 72, 40)        # main brown
    dark_brown = (80, 45, 20)    # darker shade
    light = (200, 170, 130)      # highlight

    # HEAD (rectangular robot style)
    draw.rectangle((80, 80, 320, 320), fill=brown, outline="black", width=5)

    # TOP PANEL
    draw.rectangle((140, 40, 260, 80), fill=dark_brown, outline="black", width=3)

    # SIDE PANELS (ears)
    draw.rectangle((50, 150, 80, 250), fill=dark_brown, outline="black", width=3)
    draw.rectangle((320, 150, 350, 250), fill=dark_brown, outline="black", width=3)

    # EYES (robot style big circles)
    draw.ellipse((140, 150, 180, 190), fill="white", outline="black")
    draw.ellipse((150, 160, 170, 180), fill="black")

    draw.ellipse((220, 150, 260, 190), fill="white", outline="black")
    draw.ellipse((230, 160, 250, 180), fill="black")

    # NOSE (robot line)
    draw.line((200, 200, 200, 240), fill="black", width=3)

    # MOUTH (animated)
    if mouth_open:
        draw.rectangle((170, 250, 230, 290), fill="black")
    else:
        draw.line((170, 270, 230, 270), fill="black", width=4)

    # DETAILS (robot lines)
    draw.line((100, 120, 300, 120), fill=light, width=2)
    draw.line((100, 300, 300, 300), fill=light, width=2)

    return img
