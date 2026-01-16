import streamlit as st
import streamlit as st
from pathlib import Path
import json
from models import CV
from cv_generator import generate_cv
from cv_analyzer import analyze_cv_file
from text import TRANSLATIONS


def main():
    
    translate = TRANSLATIONS["en"]
    
    st.set_page_config(
        page_title=translate["browser_title"],
        page_icon="📄",
        layout="wide"
    )
    
    st.title(translate["page_title"])
    st.markdown(translate["page_description"])
    

if __name__ == "__main__":
    main()
