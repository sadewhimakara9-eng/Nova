import streamlit as st
from groq import Groq
from PIL import Image
from mcstatus import JavaServer
import datetime
import yfinance as yf

# 1. Page Config
st.set_page_config(page_title="Nova Ultra Max V2", page_icon="🚀", layout="wide", initial_sidebar_state="expanded")

# 2. Groq API Key
client = Groq(api_key="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")

# 3. CSS - UI එක ලස්සනට සහ පැහැදිලිව හැදීම
st.markdown("""
    <style>
    .stApp { background-color: #000000 !important; }
    h1, h2, h3, p, span, div, label, .stMarkdown { color: #ffffff !important; }
    
    /* Input Boxes වල අකුරු කළු පාටින් පැහැදිලිව පේන්න */
    .stTextInput input, .stSelectbox div, .stNumberInput input, .stTextArea textarea {
        color: #000000 !important; 
        background-color: #ffffff !important;
        font-weight: bold !important;
    }
    
    .stMetric { background-color: #111111; border: 1px solid #333333; padding: 15px; border-radius: 10px; }
    section[data-testid="stSidebar"] { background-color: #050505 !important; border-right: 1px solid #444; }
    .stButton>button { background-color: #ffffff !important; color: #000000 !important; font-weight: bold !important; width: 100%; border-radius: 8px; }
    
    /* File Uploader styling */
    [data-testid="stFileUploader"] { background-color: #1a1a1a; padding: 15px; border-radius: 10px; border: 1px dashed #444; }
    </style>
    """, unsafe_allow_html=True)

# 4. SIDEBAR - මෙතනින් හැම Option එකක්ම තෝරන්න පුළුවන්
with st.sidebar:
    st.title("🚀 Nova Next-Gen")
