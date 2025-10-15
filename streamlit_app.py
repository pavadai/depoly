import streamlit as st
from PIL import Image
import numpy as np
from collections import Counter

st.title("🎨 Color Detection App")
st.write("Upload an image, then click **Detect color** to find the dominant color.")

# Upload image
uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

# Predefined simple color dictionary (name -> RGB)
NAMED_COLORS = {
    'Red': (255, 0, 0),
    'Green': (0, 255, 0),
    'Blue': (0, 0, 255),
    'Yellow': (255, 255, 0),
    'Cyan': (0, 255, 255),
    'Magenta': (255, 0, 255),
    'Black': (0, 0, 0),
    'White': (255, 255, 255),
    'Gray': (128, 128, 128),
    'Orange': (255, 165, 0),
    'Pink': (255, 192, 203),
    'Brown': (165, 42, 42)
}

# Convert RGB to HEX
def rgb_to_hex(rgb):
    return '#%02x%02x%02x' % rgb

# Find closest color name
def closest_color_name(rgb):
    r, g, b = rgb
    min_dist = float('inf')
    closest_name = ""
    for name, (cr, cg, cb) in NAMED_COLORS.items():
        dist = (r - cr)**2 + (g - cg)**2 + (b - cb)**2
        if dist < min_dist:
            min_dist = dist
            closest_name = name
    return closest_name

# Detect dominant color
def dominant_color(image):
    image = image.convert('RGB')
    arr = np.array(image)
    pixels = arr.reshape(-1, 3)
    most_common = Counter([tuple(pixel) for pixel in pixels]).most_common(1)[0][0]
    return most_common

if uploaded_file:
    img = Image.open(uploaded_file)
    st.image(img, caption="Uploaded Image", use_column_width=True)
    
    if st.button("Detect color"):
        dom_color = dominant_color(img)
        name = closest_color_name(dom_color)
        hex_color = rgb_to_hex(dom_color)
        st.write(f"**Color Name:** {name}")
        st.write(f"**RGB Values:** {dom_color}")
        st.write(f"**HEX Code:** {hex_color}")
        st.markdown(
            f"<div style='width:100%;height:100px;background-color:{hex_color};border:1px solid #000'></div>",
            unsafe_allow_html=True
        )
else:
    st.info("Please upload an image to start detecting colors.")
