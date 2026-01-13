import streamlit as st
import pandas as pd
import plotly.express as px
import gspread
from datetime import datetime
import os

# --- 1. إعدادات الصفحة ---
st.set_page_config(
    page_title="Qarar | قرار",
    page_icon="💎",
    layout="wide"
)

# --- 2. التصميم CSS ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
html, body, [class*="css"] { font-family: 'Cairo', sans-serif; }

.service-box {
    background-color: white; padding: 20px;
    border-radius: 15px; text-align: center;
    box-shadow: 0 4px 10px rgba(0,0,0,0.05);
    border-top: 5px solid #2E86C1;
    height: 200px; margin-bottom: 20px;
}
.hero-box {
    background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
    padding: 30px; border-radius: 20px;
    margin-bottom: 30px; text-align: right; direction: rtl;
}
.footer {
    position: fixed; left: 0; bottom: 0; width: 100%;
    background-color: #f1f1f1; color: #555; 
    text-align: center; padding: 10px; z-index: 100;
    font-size: 13px; border-top: 1px solid #ddd;
}
</style>
""", unsafe_allow_html=True)

# --- 3. دالة الحفظ ---
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

# --- 4. القائمة الجانبية ---
with st.sidebar:
    if os.path.exists("logo.png"):
        st.image("logo.png", use_column_width=True)
    else:
        st.image("https://cdn-icons-png.flaticon.com/512/3094/3094851.png", width=80)
    
    st.markdown("<h2 style='text-align: center; color: #2E86C1;'>منصة قرار</h2>", unsafe_allow_html=True)
    st.markdown("---")
    
    nav = st.radio("القائمة:", ["
