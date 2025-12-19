"""
Helper functions for CSS styling and image resizing
"""
import streamlit as st
from PIL import Image
from typing import Tuple

def load_css(css_file: str):
    """
    Load custom CSS from file
    
    Args:
        css_file: Path to CSS file
    """
    with open(css_file) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def resize_image(image: Image.Image, max_size: Tuple[int, int] = (800, 800)) -> Image.Image:
    """
    Resize image while maintaining aspect ratio
    
    Args:
        image: PIL Image object
        max_size: Maximum dimensions (width, height)
    
    Returns:
        Resized PIL Image
    """
    image.thumbnail(max_size, Image.Resampling.LANCZOS)
    return image

def format_confidence(score: float) -> str:
    """
    Format confidence score as percentage
    
    Args:
        score: Confidence score (0-1)
    
    Returns:
        Formatted string with percentage
    """
    return f"{score * 100:.2f}%"
