import streamlit as st
import os

def inject_premium_css():
    """Reads the custom CSS file and injects it into the Streamlit app context."""
    css_file_path = os.path.join(os.path.dirname(__file__), "assets", "style.css")
    try:
        with open(css_file_path, "r") as f:
            css_content = f.read()
            st.markdown(f"<style>{css_content}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        import logging
        logging.warning(f"Could not find CSS file at: {css_file_path}")
