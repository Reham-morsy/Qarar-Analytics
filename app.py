import streamlit as st
import pandas as pd
import plotly.express as px
import gspread
from datetime import datetime
import os

# --- 1. Settings ---
st.set_page_config(
    page_title="Qarar Analytics",
    page_icon="💎",
    layout="wide"
)

# --- 2. CSS (English LTR Styling) ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap');
html, body, [class*="css"] { font-family: 'Poppins', sans-serif; }

/* Main Colors */
h1, h2, h3 { color: #27AE60; }

/* Buttons */
div.stButton > button {
    background-color: #27AE60; color: white; border: none;
    border-radius: 8px; padding: 8px 20px; font-weight: bold;
    width: 100%; transition: 0.3s;
}
div.stButton > button:hover {
    background-color: #219150; border-color: #219150; color: white;
}

/* Service Cards */
.service-card {
    background-color: #f9f9f9; padding: 20px;
    border-radius: 10px; text-align: center;
    border-top: 4px solid #27AE60;
    box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    margin-bottom: 10px;
    height: 180px;
}

/* Footer */
.footer {
    position: fixed; left: 0; bottom: 0; width: 100%;
    background-color: #f1f1f1; color: #555; 
    text-align: center; padding: 8px; z-index: 100;
    font-size: 12px; border-top: 1px solid #ddd;
}
</style>
""", unsafe_allow_html=True)

# --- 3. Save Function (Backend) ---
def save_data(n, e):
    try:
        if "gcp_service_account" in st.secrets:
            creds = st.secrets["gcp_service_account"]
            gc = gspread.service_account_from_dict(creds)
            sh = gc.open("QararLeads")
            wks = sh.sheet1
            now = datetime.now().strftime("%Y-%m-%d %H:%M")
            wks.append_row([n, e, now])
            return True
        return False
    except:
        return False

# --- 4. Sidebar ---
with st.sidebar:
    if os.path.exists("logo.png"):
        st.image("logo.png", use_column_width=True)
    else:
        st.header("💎 Qarar")
    
    st
