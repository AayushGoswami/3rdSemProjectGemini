import streamlit as st
from PIL import Image
import os

def load_css(file_name):
    """Loads a local CSS file for custom styling."""
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def resize_image(image_path, max_width=800):
    """
    Resizes an image to a maximum width to save processing time
    while maintaining aspect ratio.
    """
    try:
        img = Image.open(image_path)
        if img.width > max_width:
            ratio = max_width / float(img.width)
            new_height = int(float(img.height) * ratio)
            img = img.resize((max_width, new_height), Image.Resampling.LANCZOS)
            img.save(image_path)
    except Exception as e:
        print(f"Error resizing image: {e}")

def render_risk_badge(risk_level):
    """Returns a color-coded HTML badge for risk levels."""
    colors = {
        "Low": "green",
        "Medium": "orange",
        "High": "red",
        "Critical": "darkred"
    }
    color = colors.get(risk_level, "gray")
    return f":{color}[{risk_level.upper()}]"